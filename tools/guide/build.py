#!/usr/bin/env python3
"""Builds the PhraseNote user guide (Korean and English) as HTML; pdf.js turns them into A4 PDFs."""
import json, html, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
META = {m['name']: m for m in json.load(open(os.path.join(HERE, 'meta.json')))}
VER = sys.argv[1] if len(sys.argv) > 1 else ''

def shot(name, width_mm=68):
    m = META[name]
    marks = ''.join(
        '<span class="mk" style="left:%.2f%%;top:%.2f%%">%d</span>' % (k['x'] / m['w'] * 100, k['y'] / m['h'] * 100, k['n'])
        for k in m['marks'])
    return '<div class="shot" style="width:%smm"><img src="img/%s.png" alt="">%s</div>' % (width_mm, name, marks)

# each section: (title, intro, [(image, width_mm)], [items], tip)
KO = dict(
    lang='ko', title='PhraseNote 사용 설명서',
    sub='폰에서 코드 진행을 칠하고, 멜로디를 쓰거나 노래로 불러, 반주·드럼과 함께 들어보는 작곡 스케치 앱',
    toc='차례', page='쪽',
    install=('시작하기', [
        '<b>앱 주소</b> https://minux22.github.io/PhraseNote/',
        '<b>삼성 인터넷</b> 메뉴(☰) → 페이지 추가 → 홈 화면 → 추가',
        '<b>크롬</b> 메뉴(⋮) → 앱 설치 또는 홈 화면에 추가',
        '설치하면 전체 화면으로 열리고, 한 번 연 뒤에는 인터넷 없이도 열립니다.',
        '<b>업데이트</b> 새 버전이 나오면 앱을 완전히 닫았다가 두 번 열면 반영됩니다. 앱 맨 아래에 버전이 보입니다.',
        '<b>자동 저장</b> 작업 내용과 녹음은 폰 안에 자동으로 보관됩니다. 다른 기기로 옮기거나 백업하려면 Save project를 쓰세요.',
    ]),
    secs=[
        ('기본 화면', '위쪽은 어느 화면에서나 같습니다.', [('main', 70)], [
            '재생 / 정지', '처음으로', 'BPM: − + 또는 숫자를 눌러 입력', '드럼 켜기·끄기', '드럼 패턴 고르기',
            '되돌리기 / 다시 실행', '박자 · 조 · 스케일', '코드 트랙 / 멜로디 트랙 전환', '믹서 열기', 'Setup: 저장과 소리 설정'],
         '아래쪽 버튼(Keys · Mixer · Setup)은 한 번에 하나만 열립니다.'),
        ('곡 구조 (Song structure)', '곡을 A, B… 섹션을 이어 붙인 슬롯으로 만듭니다.', [('form', 70)], [
            '슬롯: 탭해서 선택. 길게 누른 채 끌면 순서가 바뀝니다.',
            '+ : 새 섹션 추가, 기존 섹션 반복, 다른 프로젝트에서 가져오기',
            'Loop = 선택한 슬롯만 반복 재생 · Song = 곡 전체 재생',
            'Edit: 이 슬롯의 섹션 바꾸기, 역할(Verse · Chorus …), 이동 · 복제 · 삭제'], None),
        ('코드 입력', '팔레트에서 코드를 고르고 그리드에 칠합니다.', [('chords', 70)], [
            '팔레트: 누르면 소리가 나고 선택됩니다.',
            '그리드: 탭하거나 끌어서 칠하기. 칠한 칸을 다시 탭하면 지워집니다.',
            'Cell: 한 칸의 길이', 'Bars: 이 섹션의 마디 수',
            'Bass: 베이스 켜기·끄기 · 7th: 7화음',
            '/– : 슬래시 코드의 베이스 음',
            '주사위: 무작위 코드 진행. 이 슬롯에 멜로디가 있으면 Suggest로 바뀌어 멜로디에 맞는 진행을 제안합니다(다시 누르면 다른 안).',
            'More chords: 스케일 밖 코드'], None),
        ('반주 (Accompaniment)', '코드를 어떤 리듬과 느낌으로 칠지 고릅니다. 섹션마다 따로 정할 수 있습니다.', [('accomp', 62)], [
            '스타일: 고르면 어울리는 설정이 함께 들어갑니다.',
            'Voicing · Color · Bass: 화음 배치, 색깔음, 베이스 리듬',
            'Strum · Late: 기타처럼 흩뿌리기, 코드를 살짝 늦게',
            'Swing · Loose: 셔플 느낌, 사람 같은 흔들림'],
         '항목 이름을 누르면 짧은 도움말이 나옵니다.'),
        ('드럼', '드럼 버튼 옆 화살표로 패턴을 고릅니다.', [('drumlist', 52), ('drumgrid', 62)], [
            'My pattern을 누르면 바로 편집 창이 뜹니다.',
            '8th / 16th: 칸 해상도', 'Test: 패턴만 들어보기', 'From preset: 고른 패턴을 복사해 시작',
            '칸을 탭해 켜고 끄기. Done으로 닫기'], None),
        ('멜로디 · 피아노롤', '멜로디 트랙의 Roll 모드입니다. 위에 코드가 가이드로 보입니다.', [('roll', 70)], [
            'Mode: Roll · Staff · Audio(노래 녹음)',
            'Pickup: 못갖춘마디 추가',
            'Auto-Velocity: 멜로디 세기를 박에 맞게 자동 조절',
            '도구: 펜(탭 = 추가, 끌기 = 길이·음높이, 음 탭 = 삭제) · 선택(상자로 골라 복사·이동·삭제) · 손(스크롤)',
            'Len · Snap: 새 음 길이와 맞출 칸', '코드 줄 (오른쪽 아래 − + 버튼으로 확대·축소)'], None),
        ('멜로디 · 오선보', 'Staff 모드에서는 악보에 직접 씁니다.', [('staff', 70)], [
            '도구: 펜 · 선택 · 손',
            '음표 길이', '점음표', '임시표 (♯ ♭ ♮)'],
         '오선 위를 누른 채 위아래로 끌면 음높이를 들으며 고를 수 있습니다.'),
        ('건반으로 입력 (Keys)', '멜로디 트랙에서 Keys를 누르면 화면 건반이 열립니다.', [('keys', 64)], [
            'Live: 연주를 녹음 · Step: 누를 때마다 한 음씩 입력',
            'Rec: 켠 뒤 재생하면 1마디 카운트인 후 녹음',
            'Quant: 녹음한 음의 박자 맞춤',
            'Latency: 폰 소리 지연 보정', '◀ ▶: 건반 음역 이동'], None),
        ('박자 맞추기 · 조 추측', '', [('quant', 60), ('keyguess', 56)], [
            'Quantize의 Grid: 맞출 칸', 'Strength: 얼마나 당길지', 'Quantize all notes: 실행',
            'Key 목록 맨 위 “Guess from melody…”: 멜로디에 맞는 조 후보 3개. Apply는 조 이름만 바꾸고 음과 코드 소리는 그대로입니다.'], None),
        ('노래 녹음 (Audio)', '반주를 들으며 마이크로 녹음합니다. 유선 이어폰을 권장합니다.', [('audio', 72)], [
            'Mode에서 Audio 선택',
            '입력 장치',
            'Calibrate: 처음 한 번, 이어폰을 빼고 볼륨을 올린 채 누르면 지연을 재서 맞춰 줍니다.',
            'Input: 마이크 증폭. 숫자가 빨갛게 변하면 너무 큽니다.',
            'Loop / Song: Loop = 지정한 마디를 반복 녹음(한 바퀴마다 테이크 하나) · Song = 재생 위치부터 Stop까지',
            '반복할 마디 범위',
            'REC: 반주 1마디 뒤 녹음 시작. 다시 누르면 정지',
            '타임라인: 구간을 탭하면 그 섹션이 선택되고, 고른 테이크가 섹션마다 표시됩니다.',
            '선택한 섹션의 테이크 목록: 탭 = 이 섹션에 사용 · ▶ 듣기 · WAV 내보내기 · ✕ 삭제'],
         '녹음할 때 MIDI 멜로디를 끄려면 믹서에서 MIDI를 뮤트(M)하세요.'),
        ('Loop로 이어 쓰기', '코드 트랙을 Loop로 두고 마지막 슬롯을 선택하면, 곡 끝에 그 슬롯의 복사본이 점선으로 보입니다.', [('ghost', 70)], [
            '점선 칸에 음을 그리거나 녹음이 그 자리까지 가면 슬롯이 자동으로 늘어납니다.'],
         '앞쪽 슬롯을 Loop로 걸고 녹음하면 복사본이 그 뒤에 끼워지고, 뒤 섹션은 그만큼 밀립니다. MIDI 녹음에서 음이 없는 복사본은 녹음이 끝나면 지워집니다.'),
        ('믹서', '각 파트의 크기와 뮤트·솔로를 조절합니다. 프로젝트에 함께 저장됩니다.', [('mixer', 72)], [
            'Melody는 MIDI와 Audio(녹음)로 나뉩니다.',
            '페이더: 0.0 = 기본. 두 번 탭하면 기본값으로 돌아갑니다.',
            'M: 뮤트', 'S: 솔로(솔로를 켠 채널만 들림)', 'Rev: 리버브 양(SoundFont 소리에 적용)',
            'Master: 전체 크기',
            '레벨미터: 노랑까지가 적당, 빨강이 자주 켜지면 Master를 내리세요.'], None),
        ('저장과 열기', 'Setup의 Project에서 합니다.', [('setup_project', 66)], [
            'New project: 새 프로젝트',
            'Open project: .phrasenote 파일이나 저장한 .zip 열기',
            'Save project: 프로젝트 · MIDI · Melody.wav(섹션별로 고른 테이크를 합친 것) · 테이크별 WAV를 .zip 하나로 저장. 처음에만 이름을 묻습니다.',
            'Save as: 이름을 바꿔 새로 저장(v2, v3 …)',
            'Recent projects: 최근 10개는 폰 안에 보관'], None),
        ('소리', 'Setup의 Sound에서 합니다.', [('setup_sound', 66)], [
            'Basic Synth: 파일 없이 바로 동작 · SoundFont: 샘플 악기',
            'Load SoundFont: .sf2 파일을 불러와 트랙마다 악기 선택. 불러온 뒤에는 Save / Load preset으로 소리와 믹서 밸런스를 함께 저장할 수 있습니다.',
            '드럼 패턴과 Edit'], None),
    ],
    notes=('알아두기', [
        '사이트 데이터를 지우거나 브라우저를 삭제하면 폰 안의 프로젝트와 녹음이 사라질 수 있습니다. Save project로 자주 백업하세요.',
        '녹음은 설치한 앱(또는 앱 주소)에서 하세요. 다른 앱 안의 미리보기 화면에서는 마이크가 막힐 수 있습니다.',
        '저장 파일은 다운로드 폴더에 .zip으로 저장됩니다. 원하는 폴더에 바로 저장하는 기능은 아직 지원하지 않습니다.',
        '일부 반주 스타일과 장르 드럼은 4/4 전용입니다. 드럼·반주 패턴은 장르 느낌을 근사한 것입니다.',
    ]),
)

EN = dict(
    lang='en', title='PhraseNote User Guide',
    sub='A phone-first sketch app: paint chords, write or sing a melody, and hear it with accompaniment and drums.',
    toc='Contents', page='p.',
    install=('Getting started', [
        '<b>App address</b> https://minux22.github.io/PhraseNote/',
        '<b>Samsung Internet</b> Menu (☰) → Add page to → Home screen → Add',
        '<b>Chrome</b> Menu (⋮) → Install app or Add to Home screen',
        'Installed, it opens full screen and works offline after the first visit.',
        '<b>Updates</b> After a new version is out, close the app completely and open it twice. The version is shown at the bottom.',
        '<b>Auto-save</b> Your work and recordings are kept on the phone. Use Save project to back up or move to another device.',
    ]),
    secs=[
        ('Main screen', 'The top part is the same on every screen.', [('main', 70)], [
            'Play / Stop', 'Back to the start', 'BPM: − + or tap the number to type', 'Drums on / off', 'Choose a drum pattern',
            'Undo / Redo', 'Time · Key · Scale', 'Chord Track / Melody Track', 'Open the mixer', 'Setup: saving and sound'],
         'The bottom buttons (Keys · Mixer · Setup) open one panel at a time.'),
        ('Song structure', 'A song is a row of slots, each playing a section (A, B …).', [('form', 70)], [
            'Slot: tap to select. Long-press and drag to reorder.',
            '+ : new section, repeat a section, or import one from another project',
            'Loop = repeat the selected slot · Song = play the whole song',
            'Edit: the slot’s section, its role (Verse · Chorus …), move · duplicate · delete'], None),
        ('Chords', 'Pick a chord in the palette and paint it on the grid.', [('chords', 70)], [
            'Palette: tap to hear and select.',
            'Grid: tap or drag to paint. Tap a painted cell again to clear it.',
            'Cell: length of one cell', 'Bars: bars in this section',
            'Bass on / off · 7th: seventh chords',
            '/– : bass note of a slash chord',
            'Dice: random progression. With a melody in the slot it becomes Suggest: chords that fit the melody (tap again for another).',
            'More chords: chords outside the scale'], None),
        ('Accompaniment', 'How the chords are played. Each section can have its own.', [('accomp', 62)], [
            'Style: picking one also sets matching options.',
            'Voicing · Color · Bass: chord spacing, colour tones, bass rhythm',
            'Strum · Late: spread like a guitar, play slightly behind',
            'Swing · Loose: shuffle feel, human timing'],
         'Tap an option’s name for a short help text.'),
        ('Drums', 'The arrow next to the drum button opens the patterns.', [('drumlist', 52), ('drumgrid', 62)], [
            'My pattern opens its editor right away.',
            '8th / 16th: grid resolution', 'Test: hear the pattern alone', 'From preset: start from the chosen pattern',
            'Tap cells on and off. Done closes it.'], None),
        ('Melody · piano roll', 'Roll mode of the Melody Track. The chords are shown above as a guide.', [('roll', 70)], [
            'Mode: Roll · Staff · Audio (singing)',
            'Pickup: add a pickup bar',
            'Auto-Velocity: accents the melody on the beat',
            'Tools: Pen (tap = add, drag = length / pitch, tap a note = delete) · Select (box to copy, move, delete) · Hand (scroll)',
            'Len · Snap: new note length and grid', 'Chord lane (zoom with − + at the bottom right)'], None),
        ('Melody · staff', 'In Staff mode you write on the stave.', [('staff', 70)], [
            'Tools: Pen · Select · Hand', 'Note value', 'Dot', 'Accidental (♯ ♭ ♮)'],
         'Hold on the stave and drag up or down to hear and choose the pitch.'),
        ('Playing it in (Keys)', 'Keys opens an on-screen keyboard in the Melody Track.', [('keys', 64)], [
            'Live: record what you play · Step: one note per tap',
            'Rec: arm, then Play: one bar count-in, then recording',
            'Quant: tidy the timing of recorded notes',
            'Latency: compensate the phone’s audio delay', '◀ ▶: shift the keyboard range'], None),
        ('Quantize · key guess', '', [('quant', 60), ('keyguess', 56)], [
            'Quantize Grid: what to snap to', 'Strength: how far to pull', 'Quantize all notes: do it',
            'Top of the Key list, “Guess from melody…”: three likely keys. Apply only renames the key; notes and chords sound the same.'], None),
        ('Singing (Audio)', 'Record with the microphone over the backing. Wired earphones are recommended.', [('audio', 72)], [
            'Choose Audio in Mode',
            'Input device',
            'Calibrate: once, earphones out and volume up, to measure and correct the delay',
            'Input: microphone boost. A red number means too loud.',
            'Loop / Song: Loop = repeat the bars and record every pass as a take · Song = from the playhead until Stop',
            'Bars to loop',
            'REC: one bar of backing, then recording. Tap again to stop.',
            'Timeline: tap a section to select it; the take chosen for each section is shown.',
            'Takes of the selected section: tap = use it here · ▶ listen · WAV export · ✕ delete'],
         'To silence the MIDI melody while recording, mute MIDI (M) in the mixer.'),
        ('Keep going with Loop', 'With the Chord Track on Loop and the last slot selected, a dashed copy of that slot waits after the song.', [('ghost', 70)], [
            'Draw notes in it, or record past the end, and the song grows by itself.'],
         'Looping an earlier slot inserts the copies right after it and moves later sections back. In MIDI recording, copies left without notes are removed when you stop.'),
        ('Mixer', 'Level, mute and solo for each part. Saved with the project.', [('mixer', 72)], [
            'Melody has two channels: MIDI and Audio (recordings).',
            'Fader: 0.0 = default. Double-tap to reset.',
            'M: mute', 'S: solo (only soloed channels play)', 'Rev: reverb amount (SoundFont sounds)',
            'Master: overall level',
            'Level meter: up to yellow is right; if red lights often, lower Master.'], None),
        ('Saving and opening', 'In Setup → Project.', [('setup_project', 66)], [
            'New project',
            'Open project: a .phrasenote file or a saved .zip',
            'Save project: one .zip with the project, a MIDI file, Melody.wav (the takes chosen per section, joined) and a WAV per take. Asks for a name only the first time.',
            'Save as: a copy under a new name (v2, v3 …)',
            'Recent projects: the last 10 stay on the phone'], None),
        ('Sound', 'In Setup → Sound.', [('setup_sound', 66)], [
            'Basic Synth: works without files · SoundFont: sampled instruments',
            'Load SoundFont: load a .sf2 and pick an instrument per track. Then Save / Load preset keeps the sounds and the mixer balance together.',
            'Drum pattern and Edit'], None),
    ],
    notes=('Good to know', [
        'Clearing site data or uninstalling the browser can delete projects and recordings on the phone. Back up with Save project.',
        'Record in the installed app (or its address). Previews inside other apps may block the microphone.',
        'Files are saved to Downloads as a .zip. Saving straight into a chosen folder is not supported yet.',
        'Some accompaniment styles and genre drums are 4/4 only. Patterns approximate a genre’s feel.',
    ]),
)

CSS = r"""
*{box-sizing:border-box}
body{font-family:'Noto Sans CJK KR','Noto Sans KR','DejaVu Sans',sans-serif;color:#1b1f24;font-size:10.2pt;line-height:1.5;margin:0}
.cover{height:255mm;display:flex;flex-direction:column;justify-content:center;gap:6mm;break-after:page;background:linear-gradient(160deg,#101216,#1b1f26);color:#eceef1;border-radius:6mm;padding:0 16mm}
.cover h1{font-size:30pt;margin:0;letter-spacing:-.01em}
.cover h1 span{color:#34d3a6}
.cover p{font-size:12pt;color:#b9c0c9;margin:0;max-width:140mm}
.cover .ver{font:700 11pt 'DejaVu Sans Mono',monospace;color:#34d3a6}
.cover .row{display:flex;gap:5mm;margin-top:8mm}
.cover .row img{width:44mm;border-radius:4mm;box-shadow:0 6mm 14mm rgba(0,0,0,.5)}
h2{font-size:15pt;margin:0 0 1.5mm;display:flex;align-items:center;gap:3mm}
h2 i{font-style:normal;display:inline-grid;place-items:center;width:8mm;height:8mm;border-radius:2mm;background:#1b1f26;color:#34d3a6;font-size:11pt}
.sec{break-inside:avoid;margin:0 0 9mm}
.intro{color:#555d68;margin:0 0 3mm}
.body{display:flex;gap:7mm;align-items:flex-start}
.shots{display:flex;flex-direction:column;gap:4mm;flex:none}
.shot{position:relative;border-radius:3mm;overflow:visible;box-shadow:0 1.2mm 4mm rgba(0,0,0,.25)}
.shot img{display:block;width:100%;border-radius:3mm}
.mk{position:absolute;transform:translate(-45%,-45%);width:5.2mm;height:5.2mm;border-radius:50%;background:#ffcf33;color:#111;font:800 7.6pt/5.2mm 'DejaVu Sans',sans-serif;text-align:center;box-shadow:0 0 0 .5mm #111,0 .6mm 1.6mm rgba(0,0,0,.5)}
ol{margin:0;padding:0;list-style:none;counter-reset:n;flex:1}
ol li{counter-increment:n;position:relative;padding-left:7.5mm;margin:0 0 2.2mm}
ol li::before{content:counter(n);position:absolute;left:0;top:.3mm;width:5.2mm;height:5.2mm;border-radius:50%;background:#ffcf33;color:#111;font:800 7.6pt/5.2mm 'DejaVu Sans',sans-serif;text-align:center}
ol.plain li::before{content:'•';background:none;color:#34d3a6;font-size:12pt}
.tip{margin-top:3mm;padding:2.5mm 3.5mm;border-left:1mm solid #34d3a6;background:#eefaf6;border-radius:0 2mm 2mm 0;color:#244}
.start{break-after:page}
.toc{columns:2;column-gap:10mm;margin:4mm 0 8mm}
.toc div{break-inside:avoid;padding:1.2mm 0;border-bottom:.2mm solid #e3e6ea}
b{font-weight:700}
"""

def build(L):
    out = ['<!doctype html><html lang="%s"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>' % (L['lang'], L['title'], CSS)]
    t = L['title'].split(' ', 1)
    out.append('<section class="cover"><div class="ver">PhraseNote %s</div><h1><span>%s</span> %s</h1><p>%s</p><div class="row">%s</div></section>' % (
        VER, html.escape(t[0]), html.escape(t[1] if len(t) > 1 else ''), html.escape(L['sub']),
        ''.join('<img src="img/%s.png">' % n for n in ['main', 'audio', 'mixer'])))
    # getting started + contents
    out.append('<section class="start"><h2><i>0</i>%s</h2><ol class="plain">%s</ol>' % (L['install'][0], ''.join('<li>%s</li>' % x for x in L['install'][1])))
    out.append('<h2 style="margin-top:9mm">%s</h2><div class="toc">%s<div>%d · %s</div></div></section>' % (
        L['toc'], ''.join('<div>%d · %s</div>' % (i + 1, s[0]) for i, s in enumerate(L['secs'])), len(L['secs']) + 1, L['notes'][0]))
    for i, (title, intro, shots, items, tip) in enumerate(L['secs']):
        imgs = ''.join(shot(n, w) for n, w in shots)
        out.append('<section class="sec"><h2><i>%d</i>%s</h2>%s<div class="body"><div class="shots">%s</div><div style="flex:1"><ol>%s</ol>%s</div></div></section>' % (
            i + 1, title, ('<p class="intro">%s</p>' % intro) if intro else '', imgs,
            ''.join('<li>%s</li>' % x for x in items), ('<div class="tip">%s</div>' % tip) if tip else ''))
    out.append('<section class="sec"><h2><i>%d</i>%s</h2><ol class="plain">%s</ol></section>' % (len(L['secs']) + 1, L['notes'][0], ''.join('<li>%s</li>' % x for x in L['notes'][1])))
    out.append('</body></html>')
    open(os.path.join(HERE, L['lang'] + '.html'), 'w').write('\n'.join(out))

for L in (KO, EN):
    build(L)
print('ok')
