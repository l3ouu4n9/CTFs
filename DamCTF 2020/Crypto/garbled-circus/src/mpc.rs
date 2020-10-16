use fancy_garbling::{
    errors::TwopacError,
    twopac::semihonest::{Evaluator, Garbler, PartyId},
    Fancy, FancyInput, FancyReveal,
};
use ocelot::ot::{KosReceiver as OtReceiver, KosSender as OtSender};
use scuttlebutt::{AbstractChannel, AesRng};

fn equality_check<G: Fancy>(
    gb: &mut G,
    xs: &[G::Item],
    ys: &[G::Item],
) -> Result<G::Item, G::Error> {
    if xs.len() != ys.len() {
        return gb.constant(0, 2);
    }

    let bits_same = xs
        .iter()
        .zip(ys.iter())
        .map(|(x, y)| {
            let different = gb.xor(x, y)?;
            gb.negate(&different)
        })
        .collect::<Result<Vec<G::Item>, G::Error>>()?;
    gb.and_many(&bits_same)
}

fn convert_inputs_to_bits(inputs: &[u8]) -> Vec<u16> {
    inputs
        .iter()
        .map(|x| (0..8).map(move |i| ((x >> i) & 1) as u16))
        .flatten()
        .collect()
}

pub fn garbler<C: AbstractChannel>(mut channel: C, inputs: &[u8]) -> Result<bool, TwopacError> {
    let other_len = channel.read_u64()?;
    channel.write_u64(inputs.len() as u64)?;
    channel.flush()?;
    if other_len != inputs.len() as u64 {
        return Ok(false);
    }

    let mut gb = Garbler::<C, AesRng, OtSender>::new(channel, AesRng::new())?;

    let moduli = vec![2; 8 * inputs.len()];
    let xs = gb.encode_many(&convert_inputs_to_bits(inputs), &moduli)?;
    let ys = gb.receive_many(PartyId::Evaluator, &moduli)?;

    let eq = equality_check(&mut gb, &xs, &ys)?;
    let eq_revealed = gb.reveal(&eq)?;
    Ok(eq_revealed != 0)
}

pub fn evaluator<C: AbstractChannel>(mut channel: C, inputs: &[u8]) -> Result<bool, TwopacError> {
    channel.write_u64(inputs.len() as u64)?;
    channel.flush()?;
    let other_len = channel.read_u64()?;
    if other_len != inputs.len() as u64 {
        return Ok(false);
    }

    let mut ev = Evaluator::<C, AesRng, OtReceiver>::new(channel, AesRng::new())?;

    let moduli = vec![2; 8 * inputs.len()];
    let xs = ev.receive_many(PartyId::Garbler, &moduli)?;
    let ys = ev.encode_many(&convert_inputs_to_bits(inputs), &moduli)?;

    let eq = equality_check(&mut ev, &xs, &ys)?;
    let eq_revealed = ev.reveal(&eq)?;
    Ok(eq_revealed != 0)
}
