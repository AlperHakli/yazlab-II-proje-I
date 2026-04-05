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


---

4. KULLANILAN TEKNOLOJİLER

```md
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
![Grafana](images/grafana.png)

![WhatsApp Image 2026-04-05 at 17 38 44](https://github.com/user-attachments/assets/297e1783-63b8-4b12-83b7-c42ea1961e65)


### Loki - Log Tablosu
![Loki](images/loki.png)

## Performans ve Yük Testi

Sistem k6 aracı kullanılarak test edilmiştir. Test sırasında kullanıcı sayısı kademeli olarak artırılmıştır.

- Toplam istek: ~14,000
- Ortalama yanıt süresi: ~240 ms
- Hata oranı: %0.00

Yapılan testlerde sistemin yüksek yük altında stabil çalıştığı gözlemlenmiştir.





