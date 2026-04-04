# speedi33.github.io

# 🎡 Bar Wheel

Eine interaktive Web-App mit einem Spinning Wheel zum zufälligen Auswählen einer Bar aus einer Liste.

## Features

- 🎲 **Interaktives Spinning Wheel** mit sanfter Animation
- 📍 **Google Maps Integration** - Öffnet Google Maps mit der ausgewählten Bar
- 🗑️ **Dynamische Entfernung** - Besuchte Bars verschwinden aus dem Rad
- 📱 **Responsive Design** - Funktioniert auf allen Geräten
- ✨ **Gezinkte Reihenfolge** - Die Spins folgen einer vordefinierten Reihenfolge

## Bars im Rad

1. Eisgrub-Bräu
2. Spiritus
3. The Porter House
4. Waschmaschinensalon
5. Sixties
6. Onkel Willis Pub

## Verwendung

1. Öffne die `index.html` Datei in deinem Browser
2. Klicke auf **"SPIN!"** um das Rad zu drehen
3. Nach dem Spin klicke auf **"Navigate to Google Maps"** um die Bar auf Google Maps anzuschauen
4. Wiederhole bis alle Bars besucht wurden

## GitHub Pages Setup

Diese Seite kann auf GitHub Pages gehostet werden:

1. **Repository erstellen**: Erstelle ein neues Repository auf GitHub
2. **Code pushen**: 
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Bar Wheel App"
   git branch -M main
   git remote add origin https://github.com/DEIN-BENUTZERNAME/bar_wheel.git
   git push -u origin main
   ```
3. **GitHub Pages aktivieren**:
   - Gehe zu deinem Repository auf GitHub
   - Öffne Settings → Pages
   - Wähle `main` Branch als Source
   - Speichern
   
4. **Fertig!** Deine App ist unter `https://DEIN-BENUTZERNAME.github.io/bar_wheel` erreichbar

## Lokale Entwicklung

Du kannst die App lokal mit einem einfachen HTTP-Server testen:

```bash
# Mit Python 3
python -m http.server 8000

# Mit Python 2
python -m SimpleHTTPServer 8000

# Mit Node.js (wenn http-server installiert ist)
npx http-server
```

Dann öffne `http://localhost:8000` im Browser.

## Anpassungen

Um die Bars oder deren Farben zu ändern, bearbeite die `options` und `spinOrder` Arrays am Anfang des JavaScript-Codes in der `index.html`:

```javascript
const options = [
    { name: 'Eisgrub-Bräu', color: '#FFB347' },
    { name: 'Spiritus', color: '#FF6B6B' },
    // ... weitere Bars
];

const spinOrder = [
    'Eisgrub-Bräu',
    'Spiritus',
    // ... Reihenfolge der Spins
];
```

## Lizenz

ISC
