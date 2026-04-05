# Mikroservis Tabanlı Kütüphane Yönetim Sistemi

Bu proje, mikroservis mimarisi kullanılarak geliştirilmiş bir kütüphane yönetim sistemidir. Sistem; kullanıcı doğrulama, kitap yönetimi, ödünç alma işlemleri ve merkezi dispatcher servisi içermektedir.

## Sistem Mimarisi

```mermaid
graph TD
    Client[Client / Frontend] --> Dispatcher[Dispatcher API Gateway]

    Dispatcher --> AuthService[Auth Service]
    Dispatcher --> BookService[Book Service]
    Dispatcher --> BorrowService[Borrow Service]

    AuthService --> AuthDB[(Auth MongoDB)]
    BookService --> BookDB[(Book MongoDB)]
    BorrowService --> BorrowDB[(Borrow MongoDB)]

    Dispatcher --> Redis[(Redis Cache)]

    Dispatcher --> Prometheus[Prometheus]
    Promtail[Promtail] --> Loki[Loki]
    Prometheus --> Grafana[Grafana]
    Loki --> Grafana
```


---




## Kullanılan Teknolojiler

- Python (FastAPI)
- MongoDB
- Redis
- Docker & Docker Compose
- Prometheus
- Grafana
- Loki & Promtail
- k6 (Load Testing)

## Sistem İzleme ve Loglama

Sistem üzerinde çalışan dispatcher servisinden Prometheus metrikleri toplanmış ve Grafana ile görselleştirilmiştir.

Ayrıca container logları Promtail aracılığıyla toplanarak Loki üzerinde saklanmış ve Grafana üzerinden tablo formatında görüntülenmiştir.

## Görseller

### Grafana - İstek Grafiği
<img src="https://github.com/user-attachments/assets/39e98252-f36e-4e38-bc0f-5936a29bbd79" height="400" width="700">


### Loki - Log Tablosu
<img src="https://github.com/user-attachments/assets/7499d1f2-9274-4a5f-9a28-8290c4729031" width="600">

## Performans ve Yük Testi

Sistem k6 aracı kullanılarak test edilmiştir. Test sırasında kullanıcı sayısı kademeli olarak artırılmıştır.

- Toplam istek: ~14,000
- Ortalama yanıt süresi: ~240 ms
- Hata oranı: %0.00

Yapılan testlerde sistemin yüksek yük altında stabil çalıştığı gözlemlenmiştir.





