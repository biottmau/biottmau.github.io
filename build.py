"""Genera index.html (sitio del desarrollador, multi-idioma). Uso: python3 -I build.py
Las descripciones de Dojo Mines/Sudoku salen de las fichas de Play de cada app (../biottux_dojo*/assets/store/listing)."""
import json, os, re, html

LANGS = ['en', 'es', 'pt', 'fr', 'de', 'it', 'nl', 'pl', 'ja', 'ko', 'tr', 'hi']
NAMES = {'en': 'English', 'es': 'Español', 'pt': 'Português', 'fr': 'Français', 'de': 'Deutsch', 'it': 'Italiano',
         'nl': 'Nederlands', 'pl': 'Polski', 'ja': '日本語', 'ko': '한국어', 'tr': 'Türkçe', 'hi': 'हिन्दी'}
HERE = os.path.dirname(os.path.abspath(__file__))

def brief(app, lang):
    t = open(f'{HERE}/../biottux_{app}/assets/store/listing/listing-{lang}.md', encoding='utf-8').read()
    return re.search(r'## Descripción breve[^\n]*\n(.*?)\n', t).group(1).strip()

UI = {
 'tagline': ['Small, calm apps for Android.', 'Apps pequeñas y tranquilas para Android.', 'Apps pequenos e tranquilos para Android.', 'De petites applications sereines pour Android.', 'Kleine, ruhige Apps für Android.', 'Piccole app tranquille per Android.', 'Kleine, rustige apps voor Android.', 'Małe, spokojne aplikacje na Androida.', 'Android向けの、小さくて穏やかなアプリ。', 'Android를 위한 작고 차분한 앱.', 'Android için küçük ve sakin uygulamalar.', 'Android के लिए छोटे और शांत ऐप्स।'],
 'apps': ['My apps', 'Mis apps', 'Meus apps', 'Mes applications', 'Meine Apps', 'Le mie app', 'Mijn apps', 'Moje aplikacje', 'アプリ', '앱', 'Uygulamalarım', 'मेरे ऐप्स'],
 'privacy': ['Privacy policy', 'Política de privacidad', 'Política de privacidade', 'Politique de confidentialité', 'Datenschutzerklärung', 'Informativa sulla privacy', 'Privacybeleid', 'Polityka prywatności', 'プライバシーポリシー', '개인정보 처리방침', 'Gizlilik politikası', 'गोपनीयता नीति'],
 'contact': ['Contact', 'Contacto', 'Contato', 'Contact', 'Kontakt', 'Contatti', 'Contact', 'Kontakt', 'お問い合わせ', '문의', 'İletişim', 'संपर्क'],
 'language': ['Language', 'Idioma', 'Idioma', 'Langue', 'Sprache', 'Lingua', 'Taal', 'Język', '言語', '언어', 'Dil', 'भाषा'],
 'porotos': ['Truco scorekeeper: keep score with beans or matchsticks on a wooden table. 15 or 30 points.', 'Anotador de truco con porotos o fósforos sobre una mesa de madera. A 15 o 30 puntos.', 'Marcador de truco com feijões ou palitos de fósforo numa mesa de madeira. 15 ou 30 pontos.', 'Marqueur de truco avec des haricots ou des allumettes sur une table en bois. À 15 ou 30 points.', 'Truco-Punktezähler mit Bohnen oder Streichhölzern auf einem Holztisch. Bis 15 oder 30 Punkte.', 'Segnapunti per il truco con fagioli o fiammiferi su un tavolo di legno. A 15 o 30 punti.', 'Scoreteller voor truco met bonen of lucifers op een houten tafel. Tot 15 of 30 punten.', 'Licznik punktów do truco z fasolkami lub zapałkami na drewnianym stole. Do 15 lub 30 punktów.', '木のテーブルの上で、豆やマッチ棒を使ってトゥルーコの得点を記録。15点または30点制。', '나무 테이블 위에서 콩이나 성냥개비로 트루코 점수를 기록하세요. 15점 또는 30점제.', 'Ahşap bir masada fasulye veya kibrit çöpleriyle truco skoru tut. 15 veya 30 puan.', 'लकड़ी की मेज़ पर फलियों या माचिस की तीलियों से ट्रूको का स्कोर रखें। 15 या 30 अंक तक।'],
 'lunacycle': ['Private period & ovulation tracker. No account, data stays on your phone.', 'Agenda privada del ciclo y la ovulación. Sin cuenta, datos en tu teléfono.', 'Agenda privada do ciclo e da ovulação. Sem conta, dados no seu celular.', 'Suivi privé des règles et de l’ovulation. Sans compte, données sur votre téléphone.', 'Privater Perioden- und Eisprung-Kalender. Ohne Konto, Daten bleiben auf deinem Handy.', 'Diario privato di ciclo e ovulazione. Senza account, dati sul tuo telefono.', 'Privé cyclus- en ovulatiekalender. Geen account, gegevens blijven op je telefoon.', 'Prywatny kalendarz cyklu i owulacji. Bez konta, dane zostają w telefonie.', '月経と排卵のプライベート記録アプリ。アカウント不要、データは端末内に保存。', '비공개 생리·배란 기록 앱. 계정 없이, 데이터는 휴대폰에만 저장됩니다.', 'Özel adet ve yumurtlama takibi. Hesap yok, veriler telefonunda kalır.', 'निजी पीरियड और ओव्यूलेशन ट्रैकर। कोई खाता नहीं, डेटा आपके फ़ोन में रहता है।'],
 'nimbo': ['14-day GPS weather forecast, rain radar, alerts and a home-screen widget with clock.', 'Pronóstico del clima a 14 días por GPS, radar de lluvia, alertas y widget con hora.', 'Previsão do tempo de 14 dias por GPS, radar de chuva, alertas e widget com relógio.', 'Météo à 14 jours par GPS, radar de pluie, alertes et widget avec horloge.', '14-Tage-Wetter per GPS, Regenradar, Warnungen und ein Widget mit Uhr.', 'Meteo a 14 giorni via GPS, radar della pioggia, avvisi e widget con orologio.', '14-daagse weersverwachting via GPS, regenradar, waarschuwingen en een widget met klok.', '14-dniowa prognoza pogody z GPS, radar opadów, alerty i widżet z zegarem.', 'GPSで14日間の天気予報、雨雲レーダー、警報、時計付きウィジェット。', 'GPS 기반 14일 날씨 예보, 비 레이더, 알림, 시계 위젯.', 'GPS ile 14 günlük hava durumu, yağmur radarı, uyarılar ve saatli widget.', 'GPS से 14 दिन का मौसम पूर्वानुमान, बारिश रडार, अलर्ट और घड़ी वाला विजेट।'],
}
APPS = [  # id, nombre, ícono, repo de privacidad
 ('dojomines', 'Dojo Mines', 'dojomines', 'dojomines_privacy'),
 ('dojosudoku', 'Dojo Sudoku', 'dojosudoku', 'dojosudoku_privacy'),
 ('porotos', 'Porotos', 'porotos', 'porotos_privacy'),
 ('lunacycle', 'LunaCycle', 'lunacycle', 'lunacycle_privacy'),
 ('nimbo', 'Simple Nimbo', 'nimbo', 'simple_nimbo_privacy'),
]
for k in UI: assert len(UI[k]) == len(LANGS), k
T = {l: {k: UI[k][i] for k in UI} for i, l in enumerate(LANGS)}
for l in LANGS:
    T[l]['dojomines'] = brief('dojomines', l)
    T[l]['dojosudoku'] = brief('dojosudoku', l)

cards = '\n'.join(f'''      <article class="card">
        <img src="icons/{icon}.png" width="96" height="96" alt="" loading="lazy">
        <div><h3>{name}</h3><p data-t="{aid}">{html.escape(T['en'][aid])}</p>
        <a href="{priv}/" data-t="privacy">{T['en']['privacy']}</a></div>
      </article>''' for aid, name, icon, priv in APPS)
opts = ''.join(f'<option value="{l}">{NAMES[l]}</option>' for l in LANGS)

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Mauricio Javier Biott · Android apps</title>
<meta name="description" content="Small, calm apps for Android: Dojo Mines, Dojo Sudoku, Porotos, LunaCycle and Simple Nimbo.">
<style>
:root{{--bg:#f3f1e8;--fg:#1c2b24;--muted:#5b6b62;--card:#fff;--line:#d8d6c8;--accent:#1f6b52}}
@media(prefers-color-scheme:dark){{:root{{--bg:#101a16;--fg:#e8efe9;--muted:#9db0a5;--card:#18251f;--line:#2b3b33;--accent:#7fc4a0}}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans",sans-serif}}
main{{max-width:760px;margin:0 auto;padding:40px 20px 24px}}
header{{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap}}
h1{{margin:0;font:700 2rem/1.2 Georgia,"Noto Serif",serif}}
.tag{{margin:6px 0 0;color:var(--muted)}}
label{{font-size:.8rem;color:var(--muted);display:block;margin-bottom:2px}}
select{{background:var(--card);color:var(--fg);border:1px solid var(--line);border-radius:8px;padding:6px 8px;font:inherit}}
h2{{margin:40px 0 12px;font-size:1.1rem;letter-spacing:.04em;text-transform:uppercase;color:var(--muted)}}
.grid{{display:grid;gap:14px}}
.card{{display:flex;gap:16px;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px}}
.card img{{border-radius:22px;flex:none}}
.card h3{{margin:0 0 2px;font-size:1.15rem}}
.card p{{margin:0 0 6px;color:var(--muted)}}
a{{color:var(--accent)}}
footer{{margin-top:40px;padding-top:16px;border-top:1px solid var(--line);color:var(--muted);font-size:.9rem;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px}}
@media(max-width:480px){{.card img{{width:72px;height:72px}}}}
</style>
</head>
<body>
<main>
  <header>
    <div><h1>Mauricio Javier Biott</h1><p class="tag" data-t="tagline">{T['en']['tagline']}</p></div>
    <div><label for="lang" data-t="language">{T['en']['language']}</label><select id="lang">{opts}</select></div>
  </header>
  <section>
    <h2 data-t="apps">{T['en']['apps']}</h2>
    <div class="grid">
{cards}
    </div>
  </section>
  <footer>
    <span>© 2026 Mauricio Javier Biott</span>
    <span><span data-t="contact">{T['en']['contact']}</span>: <a href="mailto:mauro@biott.com.ar">mauro@biott.com.ar</a></span>
  </footer>
</main>
<script>
const T = {json.dumps(T, ensure_ascii=False)};
const sel = document.getElementById('lang');
function setLang(l) {{
  if (!T[l]) l = 'en';
  document.documentElement.lang = l;
  sel.value = l;
  document.querySelectorAll('[data-t]').forEach(e => {{ e.textContent = T[l][e.dataset.t]; }});
}}
const wanted = new URLSearchParams(location.search).get('lang');
const prefs = wanted ? [wanted] : (navigator.languages || [navigator.language || 'en']);
setLang(prefs.map(p => p.slice(0, 2).toLowerCase()).find(p => T[p]) || 'en');
sel.addEventListener('change', () => setLang(sel.value));
</script>
</body>
</html>
'''
open(f'{HERE}/index.html', 'w', encoding='utf-8').write(page)
print('ok', len(page), 'bytes')
