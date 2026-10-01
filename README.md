# Die Warheit: neue Ausgabe (private Entwürfe)
20 Satiren in articles.json. assets/ enthält 20 echte KI-generierte Illustrationen, sichtbar als solche beschriftet. build.py erzeugt Seiten aus einer wiederverwendbaren Vorlage, Rubriken/Startseite und SEO. base/ ist der bestehende öffentliche Stand, unverändert als Grundlage. Es gibt kein CMS-Backend.

Neuer Artikel: Datensatz mit eindeutigem slug und Thumbnail hinzufügen, python3 build.py. Quellenkasten trennt Fakten und Fiktion. Aktuelle Quellen vor Veröffentlichung erneut prüfen.

Publikation erst nach finaler Textfreigabe. Dann status=published und datePublished/dateModified auf den tatsächlichen Zeitpunkt mit Zeitzone setzen. Nicht täglich künstlich verändern. News-Sitemap nimmt nur Veröffentlichungen der letzten zwei Tage auf. Drafts sind noindex und haben kein vorgetäuschtes Veröffentlichungsdatum. Schema/SEO garantieren keine Aufnahme bei Google News.

## Live-Ausgabe Nr. 2
Die 20 Texte und Illustrationen wurden am 1. Oktober 2026 nach Prüfung freigegeben. Die GitHub-Quelle articles.json speichert die wirklichen Publikationszeiten. build.py ist die einzige Artikel-/Startseitenvorlage. assets-00.base64 bis assets-11.base64 enthalten das WebP-Archiv; der Workflow decodiert und entpackt es. Dies ist ein transportbedingter Ersatz für binäre GitHub-Uploads. Eine neue Illustration wird im Archiv ergänzt; bestehende Vorlagen bleiben erhalten. Der tägliche Pages-Build dünnt nur den News-Sitemap-Zeitraum aus und erzeugt keine neuen Texte.
