use actix_web::{web, App, HttpServer, Responder, HttpResponse};
use reqwest::Client;
use serde::{Deserialize, Serialize}; // Import Serialize
use actix_cors::Cors;
use std::sync::Arc;
use tokio::sync::Mutex;

#[derive(Deserialize, Serialize)] // Derive Serialize for JSON serialization
struct StockResponse {
    companyName: String,
    latestPrice: f64,
    symbol: String,
}

async fn get_stock(symbol: web::Path<String>, client: web::Data<Arc<Mutex<Client>>>) -> impl Responder {
    let symbol = symbol.to_uppercase();
    let url = format!("https://finance.cs50.io/quote?symbol={}", symbol);

    let client = client.lock().await;
    let response = client.get(&url).send().await;

    match response {
        Ok(resp) => {
            if resp.status().is_success() {
                match resp.json::<StockResponse>().await {
                    Ok(stock) => HttpResponse::Ok().json(stock),
                    Err(_) => HttpResponse::InternalServerError().body("Error parsing response"),
                }
            } else {
                HttpResponse::NotFound().body("Stock not found")
            }
        }
        Err(_) => HttpResponse::InternalServerError().body("Error fetching data"),
    }
}

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let client = Arc::new(Mutex::new(Client::new()));

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(client.clone()))
            .wrap(Cors::permissive())  // This line enables permissive CORS
            .route("/stock/{symbol}", web::get().to(get_stock))
    })
    .bind("127.0.0.1:8080")?
    .run()
    .await
}
