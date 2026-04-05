# Kütüphane Yönetim Sistemi - Mikroservis Mimarisi Projesi

**Ders:** Yazılım Geliştirme Laboratuvarı-II  
**Proje:** Proje - 1  
**Ekip Üyeleri:**  
- İbrahim Emir Yıldız  
- Alper Haklı  

**Tarih:** 2026
## 1. Giriş

Bu projede, mikroservis mimarisi temelli bir kütüphane yönetim sistemi geliştirilmiştir. Sistem; kullanıcı doğrulama, kitap yönetimi, ödünç alma işlemleri ve tüm dış isteklerin merkezi olarak yönlendirilmesini sağlayan bir dispatcher servisinden oluşmaktadır.

Projede amaç, monolitik yapı yerine birbirinden bağımsız çalışan servisler geliştirerek ölçeklenebilir, yönetilebilir ve güvenli bir yazılım mimarisi oluşturmaktır. Bu kapsamda sistemde bir adet dispatcher, bir adet kimlik doğrulama servisi ve en az iki işlevsel mikroservis kullanılmıştır.

Geliştirilen senaryoda kitap verileri ile ödünç alma verileri birbirinden ayrılmış, her servis kendi bağımsız veri tabanı yapısına sahip olacak şekilde tasarlanmıştır. Böylece veri izolasyonu sağlanmış, servislerin görevleri net biçimde ayrıştırılmıştır.

Ayrıca proje kapsamında dispatcher servisi üzerinden geçen trafik gözlemlenmiş, Prometheus ve Grafana ile metrikler görselleştirilmiş, Loki ile loglar tablo formatında izlenmiştir. Sistem davranışı k6 aracı ile yük testi altında incelenmiş ve sonuçlar rapora dahil edilmiştir.
## 2. Projenin Amacı

Bu projenin temel amacı, modern yazılım geliştirme süreçlerinde yaygın olarak kullanılan mikroservis mimarisini uygulamalı olarak gerçekleştirmektir. Bunun yanında tüm dış istemci trafiğini tek bir giriş noktasında toplayan dispatcher yapısının geliştirilmesi, yetkilendirme mekanizmasının merkezi hale getirilmesi ve servisler arası iletişimin doğru biçimde yönetilmesi hedeflenmiştir.

Projede ayrıca aşağıdaki kazanımlar amaçlanmıştır:

- Mikroservis mantığına uygun servis ayrımı yapmak
- Her servisin kendi veri tabanını kullanmasını sağlamak
- Dispatcher üzerinden yönlendirme ve güvenlik kontrolü gerçekleştirmek
- Sistemi Docker Compose ile tek komutta ayağa kaldırmak
- Gerçek sistem trafiğini gözlemlemek
- Yük altında sistem performansını ölçmek
## 3. Senaryo Tanımı

Projede örnek uygulama olarak bir kütüphane yönetim sistemi seçilmiştir. Bu sistemde kullanıcılar sisteme giriş yapabilmekte, kitapları görüntüleyebilmekte ve uygun durumdaki kitapları ödünç alabilmektedir. Yönetici yetkisine sahip kullanıcılar ise kitap ekleme, güncelleme ve silme işlemlerini gerçekleştirebilmektedir.

Senaryoda sistem aşağıdaki servislerden oluşmaktadır:

- **Auth Service:** Kullanıcı doğrulama ve token işlemlerini yürütür.
- **Book Service:** Kitap kayıtlarını, stok bilgisini ve kitap detaylarını yönetir.
- **Borrow Service:** Ödünç alma, iade ve kullanıcı-kitap ilişki verilerini yönetir.
- **Dispatcher:** Tüm istemci isteklerini karşılar, doğrulama ve yönlendirme işlemlerini gerçekleştirir.
## 4. Gereksinimlere Uygunluk

Sistem, proje dokümanında belirtilen gereksinimlere uygun olacak şekilde; bir dispatcher, bir auth servisi ve en az iki mikroservisten oluşacak biçimde geliştirilmiştir. Servisler birbirinden bağımsız çalışmakta, her biri kendi veri tabanı bağlantısına sahip olmakta ve tüm dış trafik dispatcher üzerinden yönlendirilmektedir. Ayrıca sistem Docker Compose ile tek komutla ayağa kaldırılabilmektedir. :contentReference[oaicite:1]{index=1} :contentReference[oaicite:2]{index=2}
