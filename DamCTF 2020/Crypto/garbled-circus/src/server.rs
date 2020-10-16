use std::{
    fs::read_to_string,
    io::{Error, ErrorKind, Result},
    net::{TcpListener, TcpStream},
    process::exit,
    thread::spawn,
};

mod mpc;

fn handle_connection(stream: Result<TcpStream>, flag: &[u8]) -> Result<()> {
    mpc::evaluator(stream?, flag)
        .map_err(|e| Error::new(ErrorKind::Other, e))?;
    Ok(())
}

fn main() -> Result<()> {
    let args = std::env::args().collect::<Vec<String>>();
    if args.len() != 2 {
        println!("Usage:");
        println!("{} <host>:<port>", args[0]);
        exit(1);
    }

    let flag = read_to_string("flag")?.trim().as_bytes().to_vec();

    let listener = TcpListener::bind(&args[1])?;
    for stream in listener.incoming() {
        let flag_ = flag.clone();
        spawn(move || {
            match handle_connection(stream, &flag_) {
                Ok(_) => {}
                Err(e) => println!("Evaluator error: {}", e)
            }
        });
    }

    Ok(())
}
