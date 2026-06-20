use tokio::net::{TcpListener, TcpStream};
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use std::error::Error;
use std::sync::Arc;

// Absorbed Environmental Configuration Drag
const LOOPBACK_INGRESS: &str = "127.0.0.1:8081"; // Pointed to by legacy app egress
const UPSTREAM_EDGE_PROXY: &str = "10.0.0.2:443"; // Modern Greenfield Track target

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    println!("[FEL SIDECAR] Initializing localized loopback mesh interface on {}", LOOPBACK_INGRESS);
    let listener = TcpListener::bind(LOOPBACK_INGRESS).await?;
    
    // Share upstream state/security context across runtime threads smoothly
    let upstream_address = Arc::new(UPSTREAM_EDGE_PROXY.to_string());

    loop {
        let (mut legacy_stream, _) = listener.accept().await?;
        let upstream_addr = Arc::clone(&upstream_address);

        tokio::spawn(async move {
            println!("[FEL SHUNT] Intercepted legacy runtime frame. Injecting upstream tunnel...");
            
            // Establish fast-path tunnel to the modern Greenfield edge proxy
            let mut modern_stream = match TcpStream::connect(&*upstream_addr).await {
                Ok(stream) => stream,
                Err(e) => {
                    eprintln!("[ERROR] Greenfield Edge proxy unreachable: {}", e);
                    return;
                }
            };

            // Non-blocking bidirectional frame splicing loop
            let (mut legacy_reader, mut legacy_writer) = legacy_stream.split();
            let (mut modern_reader, mut modern_writer) = modern_stream.split();

            let client_to_server = async {
                let mut buf = [0u8; 8192];
                loop {
                    let n = legacy_reader.read(&mut buf).await.unwrap_or(0);
                    if n == 0 { break; }
                    
                    // Macro Hook: Software Archaeologist Payload Injection Space
                    // Can inject OAuth2 headers or mutate packet specs on the fly here
                    
                    if modern_writer.write_all(&buf[..n]).await.is_err() { break; }
                }
            };

            let server_to_client = async {
                let mut buf = [0u8; 8192];
                loop {
                    let n = modern_reader.read(&mut buf).await.unwrap_or(0);
                    if n == 0 { break; }
                    if legacy_writer.write_all(&buf[..n]).await.is_err() { break; }
                }
            };

            tokio::join!(client_to_server, server_to_client);
        });
    }
}
