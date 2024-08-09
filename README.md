# Teknofest ~ Ayata AI
Teknofest Doğal Dil İşleme Yarışması için geliştirilen Ayata AI projesi, cümledeki özneleri tespit ederek, bu öznelerin olumlu, olumsuz veya nötr duygusal eğilimlerini belirler.

### Proje Tanımı
Ayata AI, bir Cümle Varlık Tanıma (NER) modeli kullanarak, verilen cümle içindeki özneleri çıkarır ve bu öznelerin olumlu, olumsuz veya nötr duygusal eğilimlerini tespit eder. Proje, doğal dil işleme (NLP) tekniklerinden faydalanarak, kullanıcıya cümlenin analizi sonucunda elde edilen duygusal değerlendirmeyi sağlar.

### Özellikler
**NER Modeli**: Cümledeki özneleri tespit eder.  
**Duygu Analizi**: Tespit edilen her bir öznenin olumlu, olumsuz veya nötr duygusal eğilimini belirler.  
**API Desteği**: FastAPI kullanılarak geliştirilen RESTful API üzerinden sonuçlara erişim sağlar.

#### API Kullanımı
**Cümle Analizi**  
Kullanıcı, POST /predict yoluna bir HTTP isteği göndererek cümle analizi gerçekleştirebilir.

Örnek İstek:
```bash
POST /predict?text=Konferansın organizasyonu çok başarılıydı, ancak konuşmacıların bazıları yetersizdi.
```

Örnek Yanıt:
```json
{
    "entity_list": [
        "Konferansın organizasyonu",
        "konuşmacıların bazıları"
    ],
    "results": [
        {
            "entity": "Konferansın organizasyonu",
            "sentiment": "olumlu"
        },
        {
            "entity": "konuşmacıların bazıları",
            "sentiment": "olumsuz"
        }
    ]
}
```
Bu örnekte, Konferansın organizasyonu öznesi olumlu olarak değerlendirilmişken, konuşmacıların bazıları öznesi olumsuz olarak değerlendirilmiştir.
