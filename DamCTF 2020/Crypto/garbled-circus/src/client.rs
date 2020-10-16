use std::{
    io::{Error, ErrorKind, Result},
    net::TcpStream,
    process::exit,
};

mod mpc;

fn main() -> Result<()> {
    let args = std::env::args().collect::<Vec<String>>();
    if args.len() != 3 {
        println!("Usage:");
        println!("{} <host>:<port> <flag_guess>", args[0]);
        exit(1);
    }

    let channel = TcpStream::connect(&args[1])?;

    let eq = mpc::garbler(channel, &args[2].as_bytes())
        .map_err(|e| Error::new(ErrorKind::Other, e))?;

    if eq {
        println!("Correct!");
    } else {
        println!("Guess again.");
    }

    Ok(())
}
