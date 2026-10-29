#!/usr/bin/env python3
"""Builds the PhraseNote user guide (Korean and English) as HTML; pdf.js turns them into A4 PDFs.
Screenshots and marker positions come from cap.js (img/*.png, meta.json)."""
import json, html, sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
META = {m['name']: m for m in json.load(open(os.path.join(HERE, 'meta.json')))}
VER = sys.argv[1] if len(sys.argv) > 1 else ''
D = 5.4  # marker diameter, mm

def place(m, wmm):
    """marker centres in mm, nudged so that no two overlap"""
    hmm = wmm * m['h'] / m['w']
    out = []
    for k in sorted(m['marks'], key=lambda k: k['n']):
        x, y = k['x'] / m['w'] * wmm, k['y'] / m['h'] * hmm
        x = max(D / 2 - 1, x); y = max(D / 2 - 1, y)
        tries = 0
        while any(math.hypot(x - a, y - b) < D + .3 for a, b, _ in out) and tries < 40:
            x += D * .55
            if x > wmm - D / 2 + 1:
                x = k['x'] / m['w'] * wmm; y += D * .7
            tries += 1
        out.append((x, y, k['n']))
    return out, hmm

def shot(name, wmm):
    m = META[name]
    pts, hmm = place(m, wmm)
    marks = ''.join('<span class="mk" style="left:%.2fmm;top:%.2fmm">%d</span>' % (x, y, n) for x, y, n in pts)
    return '<div class="shot" style="width:%smm;height:%.2fmm"><img src="img/%s.png" alt="">%s</div>' % (wmm, hmm, name, marks)

# parts: (part title, [sections]); section: (title, intro, [(image, width)], [items], tip)
KO = dict(
    lang='ko', title='PhraseNote 사용 설명서',
    sub='폰에서 코드 진행을 칠하고, 멜로디를 쓰거나 노래로 불러, 반주·드럼과 함께 들어보는 작곡 스케치 앱',
    toc='차례',
    install=('시작하기', [
        '<b>앱 주소</b> https://minux22.github.io/PhraseNote/',
        '<b>삼성 인터넷으로 설치</b> 앱 주소를 열고 메뉴(☰, 오른쪽 아래) → 페이지 추가 → 홈 화면 → 추가. 주소창에 설치 아이콘이 보이면 그걸 눌러도 됩니다.',
        '<b>크롬으로 설치</b> 앱 주소를 열고 메뉴(⋮, 오른쪽 위) → 앱 설치 또는 홈 화면에 추가 → 설치.',
        '설치하면 홈 화면 아이콘으로 전체 화면에서 열리고, 한 번 연 뒤에는 인터넷 없이도 열립니다.',
        '<b>업데이트</b> 새 버전이 나오면 앱을 완전히 닫았다가 두 번 열면 반영됩니다(첫 번째에 내려받고 두 번째에 적용). 화면 맨 아래에 버전이 보입니다.',
        '<b>자동 저장</b> 작업 내용과 녹음은 편집할 때마다 폰 안에 자동으로 보관됩니다. 백업하거나 다른 기기로 옮길 때는 Setup의 Save project로 파일을 만드세요.',
        '<b>기본 흐름</b> 코드 트랙에서 코드 진행과 반주·드럼을 만들고 → 멜로디 트랙에서 멜로디를 쓰거나 노래로 녹음하고 → 믹서로 밸런스를 맞춘 뒤 → Save project로 저장합니다.',
    ]),
    parts=[
    ('코드 트랙', [
        ('기본 화면', '화면 위쪽은 코드 트랙과 멜로디 트랙에서 똑같이 쓰입니다.', [('main', 70)], [
            '재생 / 정지. 재생 위치(흰 선)부터 시작합니다.',
            '처음으로: 재생 위치를 곡의 처음으로 옮깁니다.',
            'BPM: − + 로 1씩 바꾸거나 숫자를 눌러 직접 입력합니다(40~200).',
            '드럼 켜기·끄기. 켜면 선택한 드럼 패턴이 함께 연주됩니다.',
            '드럼 패턴 목록 열기(5. 드럼 참고).',
            '되돌리기 / 다시 실행. 코드·멜로디·곡 구조 편집을 되돌립니다.',
            '박자 · 조 · 스케일. 조 목록 맨 위의 “Guess from melody…”는 멜로디로 조를 추측합니다(10장).',
            '코드 트랙 / 멜로디 트랙 전환. 재생 중에 바꿔도 끊기지 않습니다.',
            '믹서 열기(13장).', 'Setup 열기: 저장, 열기, 소리 설정(14·15장).'],
         '아래쪽 버튼(Keys · Mixer · Setup)은 한 번에 하나만 열립니다. 다른 버튼을 누르면 열려 있던 것은 닫힙니다.'),
        ('곡 구조 (Song structure)', '곡은 A, B… 섹션을 담은 슬롯을 순서대로 이어서 만듭니다. 같은 섹션을 여러 슬롯에 반복해서 쓸 수 있습니다.', [('form', 70)], [
            '슬롯: 탭하면 선택되고, 아래 코드 그리드에 그 섹션이 열립니다. 길게 누른 채 옆으로 끌면 순서를 바꿀 수 있습니다.',
            '+ : 슬롯 추가. 새 섹션 만들기, 기존 섹션 반복, 다른 프로젝트 파일에서 섹션 가져오기 중에서 고릅니다. 새 섹션은 지금 섹션과 같은 길이로 만들어집니다.',
            'Loop / Song: Loop는 선택한 슬롯만 반복해서 들려주고, Song은 곡 전체를 처음부터 끝까지 들려줍니다. 멜로디 트랙에서 Loop가 하는 일은 12장을 보세요.',
            'Edit: 선택한 슬롯의 섹션 바꾸기, 역할 붙이기(Intro · Verse · Pre · Chorus · Bridge · Outro), 앞뒤로 이동 · 복제 · 삭제.'], None),
        ('코드 입력', '팔레트에서 코드를 고르고 그리드에 칠합니다. 지금 선택한 섹션의 코드가 보입니다.', [('chords', 70)], [
            '팔레트: 현재 조와 스케일의 코드가 로마 숫자와 코드 이름으로 나옵니다. 누르면 소리가 나며 선택되고, Erase는 지우개입니다.',
            '그리드: 칸을 탭하거나 손가락으로 끌어서 선택한 코드를 칠합니다. 이미 칠한 칸을 다시 탭하면 지워집니다.',
            'Cell: 한 칸의 길이(한 마디 · 2박 · 1박). 코드가 바뀌는 간격입니다.',
            'Bars: 이 섹션의 마디 수(2 · 4 · 8 · 16).',
            'Bass: 베이스 파트 켜기·끄기. 7th: 모든 코드를 7화음으로.',
            '/– : 슬래시 코드. 베이스로 칠 스케일 음을 고른 뒤 칸을 칠하면 그 음이 베이스가 됩니다.',
            '주사위(Random): 무작위 코드 진행으로 섹션을 채웁니다. 이 슬롯에 멜로디가 있으면 반짝이 버튼(Suggest)으로 바뀌어 멜로디에 어울리는 진행을 제안합니다(10장).',
            'More chords: 스케일 밖의 코드(빌려 온 코드, 세컨더리 도미넌트 등)를 펼칩니다.'],
         '마음에 들지 않으면 위쪽 되돌리기로 언제든 이전 진행으로 돌아갈 수 있습니다.'),
        ('반주 (Accompaniment)', '코드를 어떤 리듬과 느낌으로 연주할지 정합니다. 섹션마다 다르게 정할 수 있습니다(예: Verse는 Arp, Chorus는 Strum).', [('accomp', 62)], [
            '스타일: Classic · Modern · Jazz/Soul · Rock/Folk 그룹에서 고릅니다. 고르면 그 스타일에 어울리는 아래 설정이 함께 바뀝니다.',
            'Voicing · Color · Bass: 화음을 쌓는 방식(가깝게·넓게·부드럽게 잇기), 색깔음(add9 · sus · 6/9 · 9th), 베이스 리듬(근음 · 근음+5도 · 옥타브 · 킥에 맞춤).',
            'Strum · Late: 기타처럼 음을 살짝 흩어서 치기, 코드만 박보다 조금 늦게 치기.',
            'Swing · Loose: 8분/16분 셔플 느낌, 사람이 친 것처럼 타이밍을 약간 흔들기.'],
         '항목 이름(밑줄 친 글자)을 누르면 짧은 도움말이 나옵니다. 일부 스타일은 4/4에서만 동작합니다.'),
        ('드럼', '드럼 버튼 옆 화살표를 누르면 패턴 목록이 열립니다. 패턴도 섹션마다 따로 정해집니다.', [('drumlist', 52), ('drumgrid', 62)], [
            '목록에서 패턴을 누르면 바로 들려주고 드럼이 켜집니다. 맨 아래 My pattern을 누르면 직접 만드는 편집 창이 열립니다.',
            '8th / 16th: 한 마디를 8칸 또는 16칸으로 나눕니다.',
            'Test: 반주 없이 드럼 패턴만 반복해서 들려줍니다.',
            'From preset: 목록에서 마지막으로 고른 패턴을 복사해서 시작합니다. Clear는 모두 지웁니다.',
            '악기 줄(킥 · 스네어 · 사이드스틱 · 하이햇 · 오픈햇 · 라이드 · 클랩)의 칸을 탭해서 켜고 끕니다. Done으로 닫습니다.'], None),
    ]),
    ('멜로디 트랙', [
        ('피아노롤 (Roll)', '멜로디 트랙의 기본 화면입니다. 위쪽 코드 줄에 코드 트랙의 진행이 가이드로 나옵니다.', [('roll', 70)], [
            'Mode: Roll(피아노롤) · Staff(오선보) · Audio(노래 녹음)를 바꿉니다. 재생 중에 바꿔도 끊기지 않습니다.',
            'Pickup: 곡 앞에 못갖춘마디를 하나 붙입니다.',
            'Auto-Velocity: 멜로디의 세기를 박에 맞춰 자동으로 강약을 줍니다(0% = 일정, 100% = 최대).',
            '도구 — 펜: 빈 곳을 탭하면 음 추가, 끌면 길이·음높이 조절, 음을 탭하면 삭제. 선택: 상자로 여러 음을 골라 복사 · 붙여넣기 · 이동 · 옥타브 이동 · 삭제. 손: 편집하지 않고 화면만 움직이기.',
            'Len · Snap: 새로 넣을 음의 길이와, 음이 맞춰질 박 단위.',
            '코드 줄: 해당 마디의 코드와 섹션 이름. 아래 − + 버튼으로 가로 확대·축소합니다.'], None),
        ('오선보 (Staff)', '같은 멜로디를 악보로 보고 직접 씁니다.', [('staff', 70)], [
            '도구: 펜 · 선택 · 손(롤과 같음).',
            '음표 길이: 온음표부터 16분음표까지. 먼저 고른 뒤 오선을 누릅니다.',
            '점음표: 고른 음표를 1.5배 길이로.',
            '임시표: ♯ ♭ ♮를 붙여서 넣습니다.'],
         '오선 위를 누른 채 위아래로 끌면 음높이를 들으며 고를 수 있고, 손을 떼면 그 자리에 들어갑니다. 선택 도구로 고른 음은 ▲▼(반음) ◀▶(16분음표)로 옮길 수 있습니다.'),
        ('건반으로 입력 (Keys)', '하단 Keys를 누르면 화면 건반이 열립니다. Roll · Staff 모드에서 쓸 수 있습니다.', [('keys', 64)], [
            'Live / Step: Live는 연주를 실시간으로 녹음하고, Step은 건반을 누를 때마다 한 음씩 차례로 넣습니다(길이는 Len).',
            'Rec: 켜 두고 재생을 누르면 1마디 카운트인 뒤 녹음됩니다(Count-in으로 끌 수 있음).',
            'Quant: 녹음한 음을 고른 박(16 · 8 · 4분)에 맞춥니다.',
            'Latency: 폰의 소리 지연을 재서 녹음 타이밍을 맞춥니다. 처음 한 번 해 두면 좋습니다.',
            '◀ ▶: 건반 음역을 옮깁니다.'], None),
        ('박자 맞추기 (Quantize)', '이미 들어간 음 전체의 타이밍을 정리합니다. 멜로디 아래 Quantize를 열어 씁니다.', [('quant', 62)], [
            'Grid: 맞출 박 단위(32분 ~ 4분, 셋잇단 16T · 8T).',
            'Strength: 얼마나 당길지(100% = 정확히 박에, 50% = 절반만).',
            'Quantize all notes: 실행합니다. Length를 켜면 음 길이도 함께 맞춥니다.'], None),
        ('멜로디로 조와 코드 찾기', '멜로디를 먼저 쓴 경우, 앱이 멜로디에 맞는 조와 코드를 제안합니다.', [('keyguess', 56), ('suggest', 62)], [
            '조 추측: Key 목록 맨 위 “Guess from melody…”를 고르면 어울리는 조 후보 3개가 나옵니다. Apply는 조 이름만 바꾸고, 멜로디와 코드 소리는 그대로입니다.',
            'Suggest: 멜로디가 있는 슬롯에서는 코드 트랙의 주사위가 반짝이 버튼으로 바뀝니다. 누르면 그 멜로디에 맞춰 빈칸에 코드를 채우고, 다시 누를 때마다 다른 안(최대 5개)을 보여줍니다.'], None),
        ('노래 녹음 (Audio)', 'Mode에서 Audio를 고르면 반주를 들으며 마이크로 녹음할 수 있습니다. 반주가 마이크에 들어가지 않도록 유선 이어폰을 권장합니다.', [('audio', 72)], [
            'Mode에서 Audio 선택. 이때 마이크가 켜지고, 다른 모드로 가면 꺼집니다.',
            '입력 장치: 보통은 그대로 두면 됩니다.',
            'Calibrate: 처음 한 번, 이어폰을 빼고 볼륨을 올린 채 누르세요. 스피커의 클릭을 마이크로 다시 받아 지연을 재고 녹음 위치를 맞춰 줍니다.',
            'Input: 마이크 소리 키우기. 가장 크게 부를 때 아래 미터가 주황 근처까지 오도록 맞추고, 숫자가 빨갛게 변하면 내립니다.',
            'Loop / Song: Loop는 지정한 마디를 계속 반복하며 한 바퀴마다 테이크를 하나씩 쌓고, Song은 재생 위치부터 Stop을 누를 때까지 한 번에 녹음합니다.',
            '반복할 마디: Loop일 때 시작 마디와 끝 마디(끝 마디 포함). 재생할 때도 이 구간이 반복되고 구간 밖은 어둡게 보입니다.',
            'REC: 반주가 1마디 나온 뒤 녹음이 시작됩니다. 다시 누르면 멈추고 테이크가 저장됩니다.',
            '타임라인: 구간(섹션)을 탭하면 그 섹션이 선택되고 재생 위치도 옮겨집니다. 섹션마다 고른 테이크가 각자 자리에 표시되고 함께 재생됩니다.',
            '선택한 섹션의 테이크 목록: 행을 탭하면 이 섹션에 그 테이크를 씁니다(다시 탭하면 해제). ▶ 이 섹션부터 듣기 · WAV 내보내기 · ✕ 삭제(되돌리기 가능).'],
         '테이크 이름은 Song-Bar01-1st, Loop-Bar01-04-2nd처럼 시작 마디와 순번으로 붙습니다. 녹음 중에 MIDI 멜로디를 듣지 않으려면 믹서에서 MIDI를 뮤트하세요.'),
        ('Loop로 이어 쓰기', '코드 트랙을 Loop로 두면 멜로디 트랙에서도 선택한 슬롯이 반복됩니다. 그 위에서 멜로디를 계속 이어 쓰면 슬롯이 자동으로 늘어납니다.', [('ghost', 70)], [
            '마지막 슬롯을 선택하면 곡 끝에 그 슬롯의 복사본이 점선으로 미리 보입니다. 거기에 음을 그리면 실제 슬롯으로 바뀌고, 다음 점선 칸이 또 생깁니다.',
            '녹음(노래나 Keys 실시간)은 슬롯 끝에서 되돌아가지 않고, 다음 복사본을 미리 만들어 둔 채 계속 이어집니다.',
            '앞쪽 슬롯을 Loop로 걸면 복사본이 그 바로 뒤에 끼워지고, 뒤 섹션과 그 멜로디는 그만큼 뒤로 밀립니다.',
            'Keys 녹음에서 음이 하나도 없는 복사본은 녹음이 끝나면 지워집니다. 노래 녹음은 지나간 만큼 남습니다.'], None),
    ]),
    ('소리와 저장', [
        ('믹서', '하단 Mixer를 누르면 열립니다. 파트별 크기와 뮤트·솔로를 정하고, 프로젝트에 함께 저장됩니다.', [('mixer', 72)], [
            '채널: Melody MIDI(음표 멜로디) · Melody Audio(녹음한 노래) · Chords · Bass · Drums.',
            '페이더: 위아래로 끌어 크기를 조절합니다. 0.0 dB가 기본이고 위로 +12 dB까지. 두 번 탭하면 기본값으로 돌아갑니다. 눈금을 지날 때마다 짧게 진동합니다.',
            'M(뮤트): 이 채널을 끕니다.',
            'S(솔로): 솔로를 켠 채널만 들립니다. 여러 개를 함께 켤 수 있습니다.',
            'Rev: 리버브 양(SoundFont 소리에 적용).',
            'Master: 전체 크기.',
            '레벨미터: 실제로 나가는 소리의 크기. 노랑 구간 안이 적당하고, 맨 위 빨강이 자주 켜지면 Master를 내리세요. 아래 숫자는 최근 최고 레벨입니다.'],
         'MIDI 파일에도 각 트랙의 페이더 값이 볼륨으로 들어갑니다.'),
        ('소리 (SoundFont)', 'Setup의 Sound에서 악기 소리를 고릅니다.', [('setup_sound', 66)], [
            'Basic Synth는 파일 없이 바로 동작하는 기본 소리, SoundFont는 실제 악기 샘플 소리입니다.',
            'Load SoundFont: .sf2 파일(예: GeneralUser GS)을 불러오면 Melody · Chords · Bass · Drums마다 악기를 고를 수 있습니다. 불러온 파일은 폰에 보관됩니다. 불러온 뒤에는 Save / Load preset으로 악기 선택과 믹서 밸런스를 함께 저장하고 불러올 수 있습니다.',
            '드럼 패턴 선택과 Edit(5장의 편집 창).'], None),
        ('저장과 열기', 'Setup의 Project에서 합니다.', [('setup_project', 66)], [
            'New project: 새 프로젝트를 시작합니다(두 번 눌러 확인).',
            'Open project: 저장한 .zip이나 .phrasenote 파일을 엽니다. 녹음도 함께 복원됩니다.',
            'Save project: 다운로드 폴더에 .zip 하나로 저장합니다. 안에는 프로젝트 파일, MIDI 파일, Melody.wav(섹션별로 고른 테이크를 합친 멜로디 오디오), 테이크별 WAV가 들어 있습니다. 이름은 처음에만 묻고, 그다음부터는 바로 덮어씁니다.',
            'Save as: 지금 내용을 다른 이름으로 새로 저장합니다. 기본 이름은 My Song v2, v3…처럼 붙습니다.',
            'Recent projects: 최근 작업한 10개가 폰에 보관되어 바로 열 수 있습니다.'],
         'MIDI 파일은 Chords · Bass · Melody · Drums(드럼이 켜져 있을 때)가 트랙별로 나뉘어 DAW에서 바로 이어서 작업할 수 있습니다.'),
    ]),
    ],
    notes=('알아두기', [
        '앱 안의 데이터는 브라우저 저장공간에 있습니다. 사이트 데이터를 지우거나 브라우저를 삭제하면 사라질 수 있으니 Save project로 자주 백업하세요.',
        '녹음은 설치한 앱이나 앱 주소에서 하세요. 다른 앱 안의 미리보기 화면에서는 마이크가 막힐 수 있습니다. 마이크 권한을 거부했다면 브라우저의 사이트 설정에서 다시 허용하세요.',
        '블루투스 이어폰은 지연이 커서 녹음에 맞지 않습니다. 유선 이어폰을 권장합니다.',
        '저장 파일은 다운로드 폴더에 .zip으로 저장됩니다. 원하는 폴더에 바로 저장하는 기능은 아직 지원하지 않습니다.',
        '일부 반주 스타일과 장르 드럼은 4/4 전용이며, 패턴은 장르의 느낌을 근사한 것입니다.',
    ]),
)

EN = dict(
    lang='en', title='PhraseNote User Guide',
    sub='A phone-first sketch app: paint chords, write or sing a melody, and hear it with accompaniment and drums.',
    toc='Contents',
    install=('Getting started', [
        '<b>App address</b> https://minux22.github.io/PhraseNote/',
        '<b>Install with Samsung Internet</b> Open the address, then Menu (☰, bottom right) → Add page to → Home screen → Add. If an install icon shows in the address bar, that works too.',
        '<b>Install with Chrome</b> Open the address, then Menu (⋮, top right) → Install app or Add to Home screen → Install.',
        'Installed, it opens full screen from its home-screen icon and works offline after the first visit.',
        '<b>Updates</b> After a new version is out, close the app completely and open it twice (the first opening downloads it, the second uses it). The version is shown at the bottom.',
        '<b>Auto-save</b> Your work and recordings are kept on the phone as you edit. To back up or move to another device, make a file with Save project in Setup.',
        '<b>The usual flow</b> Build the chords, accompaniment and drums in the Chord Track → write or sing the melody in the Melody Track → balance it in the mixer → Save project.',
    ]),
    parts=[
    ('Chord Track', [
        ('Main screen', 'The top part works the same in the Chord Track and the Melody Track.', [('main', 70)], [
            'Play / Stop, from the playhead (white line).',
            'Back to the start of the song.',
            'BPM: − + steps by one, or tap the number to type (40–200).',
            'Drums on / off. On, the chosen pattern plays along.',
            'Open the drum pattern list (see 5. Drums).',
            'Undo / Redo for chords, melody and song structure.',
            'Time · Key · Scale. “Guess from melody…” at the top of the Key list guesses the key (chapter 10).',
            'Chord Track / Melody Track. Switching does not stop playback.',
            'Open the mixer (chapter 13).', 'Open Setup: saving, opening, sound (chapters 14 · 15).'],
         'The bottom buttons (Keys · Mixer · Setup) open one panel at a time; opening one closes the other.'),
        ('Song structure', 'A song is a row of slots, each playing a section (A, B …). The same section can be used in several slots.', [('form', 70)], [
            'Slot: tap to select; the chord grid below shows its section. Long-press and drag sideways to reorder.',
            '+ : add a slot — a new section, a repeat of one, or a section imported from another project file. New sections take the current length.',
            'Loop / Song: Loop repeats the selected slot, Song plays the whole song. For Loop in the Melody Track see chapter 12.',
            'Edit: change the slot’s section, give it a role (Intro · Verse · Pre · Chorus · Bridge · Outro), move, duplicate or delete.'], None),
        ('Chords', 'Pick a chord in the palette and paint it on the grid of the selected section.', [('chords', 70)], [
            'Palette: the chords of the key and scale, as numerals and names. Tap to hear and select; Erase is the eraser.',
            'Grid: tap or drag to paint. Tap a painted cell again to clear it.',
            'Cell: length of one cell (bar · 2 beats · beat) — how often chords can change.',
            'Bars: length of this section (2 · 4 · 8 · 16).',
            'Bass: bass part on / off. 7th: all chords as sevenths.',
            '/– : slash chords. Pick the scale note for the bass, then paint.',
            'Dice (Random): fill the section with a random progression. With a melody in the slot it becomes a sparkle button (Suggest) that proposes chords for the melody (chapter 10).',
            'More chords: chords outside the scale (borrowed chords, secondary dominants …).'],
         'Not happy? Undo brings the previous progression back at any time.'),
        ('Accompaniment', 'How the chords are played. Each section can have its own (e.g. arpeggios in the verse, strumming in the chorus).', [('accomp', 62)], [
            'Style: Classic · Modern · Jazz/Soul · Rock/Folk. Picking one also sets the options below to suit it.',
            'Voicing · Color · Bass: how the chord is stacked (close · open · spread · smooth), colour tones (add9 · sus · 6/9 · 9th), bass rhythm (root · root+5 · octave · on the kick).',
            'Strum · Late: spread the notes like a guitar, play the chords slightly behind the beat.',
            'Swing · Loose: 8th/16th shuffle, a little human timing.'],
         'Tap an option’s underlined name for a short help text. Some styles are 4/4 only.'),
        ('Drums', 'The arrow next to the drum button opens the patterns. Each section keeps its own pattern.', [('drumlist', 52), ('drumgrid', 62)], [
            'Tap a pattern to hear it and turn the drums on. My pattern, at the bottom, opens its editor.',
            '8th / 16th: 8 or 16 steps per bar.',
            'Test: play the pattern alone, in a loop.',
            'From preset: start from the pattern last picked in the list. Clear empties it.',
            'Tap cells on each row (kick · snare · side stick · hi-hat · open hat · ride · clap). Done closes it.'], None),
    ]),
    ('Melody Track', [
        ('Piano roll (Roll)', 'The Melody Track’s main view. The chord lane on top shows the Chord Track as a guide.', [('roll', 70)], [
            'Mode: Roll · Staff · Audio (singing). Switching does not stop playback.',
            'Pickup: add a pickup bar before the song.',
            'Auto-Velocity: accents the melody on the beat (0% = flat, 100% = strongest).',
            'Tools — Pen: tap empty space to add, drag to change length or pitch, tap a note to delete. Select: draw a box, then copy · paste · move · octave · delete. Hand: scroll without editing.',
            'Len · Snap: length of new notes, and the grid they snap to.',
            'Chord lane: chords and section names per bar. − + at the bottom right zoom in and out.'], None),
        ('Staff', 'The same melody as notation, written directly.', [('staff', 70)], [
            'Tools: Pen · Select · Hand (as in the roll).',
            'Note value: whole to sixteenth. Pick it, then tap the stave.',
            'Dot: one and a half times as long.',
            'Accidental: ♯ ♭ ♮.'],
         'Hold on the stave and drag up or down to hear the pitch; let go to place it. Selected notes move with ▲▼ (semitone) and ◀▶ (sixteenth).'),
        ('Playing it in (Keys)', 'Keys at the bottom opens an on-screen keyboard (Roll and Staff modes).', [('keys', 64)], [
            'Live / Step: Live records what you play in time; Step adds one note per key press (length = Len).',
            'Rec: arm it, then Play: one bar count-in, then recording (Count-in can be switched off).',
            'Quant: snap recorded notes to 16ths, 8ths or quarters.',
            'Latency: measure the phone’s audio delay so recordings line up. Worth doing once.',
            '◀ ▶: shift the keyboard range.'], None),
        ('Quantize', 'Tidies the timing of all notes. Open Quantize under the melody.', [('quant', 62)], [
            'Grid: what to snap to (32nd to quarter, triplets 16T · 8T).',
            'Strength: how far to pull (100% = exactly on the grid, 50% = half way).',
            'Quantize all notes: do it. With Length on, note lengths are tidied too.'], None),
        ('Key and chords from the melody', 'Wrote the melody first? The app suggests a key and chords that fit it.', [('keyguess', 56), ('suggest', 62)], [
            'Key guess: “Guess from melody…” at the top of the Key list shows three likely keys. Apply only renames the key; the melody and chords sound the same.',
            'Suggest: in a slot with melody, the Chord Track’s dice becomes a sparkle button. Tap it to fill empty cells with chords that fit the melody; tap again for another option (up to five).'], None),
        ('Singing (Audio)', 'Choose Audio in Mode to record with the microphone over the backing. Wired earphones keep the backing out of the recording.', [('audio', 72)], [
            'Audio in Mode. The microphone is on in this mode only.',
            'Input device: usually leave as it is.',
            'Calibrate: once, earphones out and volume up. The speaker’s clicks are recorded back to measure the delay, and recordings are placed accordingly.',
            'Input: microphone boost. Sing your loudest part and aim for the meter below to reach about orange; if the number turns red, lower it.',
            'Loop / Song: Loop repeats the bars you set and keeps every pass as a take; Song records from the playhead until Stop.',
            'Bars to loop: first and last bar (inclusive). Playback loops them too; outside is dimmed.',
            'REC: one bar of backing, then recording. Tap again to stop and keep the take.',
            'Timeline: tap a section to select it (the playhead moves there too). The take chosen for each section is shown in place, and they play together.',
            'Takes of the selected section: tap a row to use that take here (tap again to un-use). ▶ listen from this section · WAV export · ✕ delete (Undo brings it back).'],
         'Takes are named like Song-Bar01-1st or Loop-Bar01-04-2nd. To silence the MIDI melody while recording, mute MIDI in the mixer.'),
        ('Keep going with Loop', 'With the Chord Track on Loop, the Melody Track repeats the selected slot too, and the song grows as you keep writing.', [('ghost', 70)], [
            'Select the last slot and a dashed copy of it waits after the song. Draw notes in it and it becomes real, with a new dashed copy after it.',
            'Recording (singing or Keys Live) does not jump back at the end of the slot: the next copy is made ahead of time and recording carries on.',
            'Looping an earlier slot inserts the copies right after it; later sections and their melody move back.',
            'Copies left without notes after a Keys recording are removed when you stop. Singing keeps the copies it passed.'], None),
    ]),
    ('Sound and saving', [
        ('Mixer', 'Mixer at the bottom opens it. Level, mute and solo per part; saved with the project.', [('mixer', 72)], [
            'Channels: Melody MIDI (notes) · Melody Audio (recordings) · Chords · Bass · Drums.',
            'Fader: drag up or down. 0.0 dB is the default, up to +12 dB. Double-tap to reset. A short buzz marks each tick.',
            'M (mute): silence the channel.',
            'S (solo): only soloed channels play; several can be soloed.',
            'Rev: reverb amount (SoundFont sounds).',
            'Master: overall level.',
            'Level meter: what actually comes out. Inside yellow is right; if the top red lights often, lower Master. The number is the recent peak.'],
         'MIDI files carry each track’s fader as its volume.'),
        ('Sound (SoundFont)', 'In Setup → Sound.', [('setup_sound', 66)], [
            'Basic Synth works without files; SoundFont plays sampled instruments.',
            'Load SoundFont: load a .sf2 file (e.g. GeneralUser GS) and pick an instrument for Melody · Chords · Bass · Drums. Loaded files stay on the phone. Then Save / Load preset stores the instruments together with the mixer balance.',
            'Drum pattern and Edit (the editor from chapter 5).'], None),
        ('Saving and opening', 'In Setup → Project.', [('setup_project', 66)], [
            'New project (tap twice to confirm).',
            'Open project: a saved .zip or .phrasenote file. Recordings come back too.',
            'Save project: one .zip in Downloads with the project file, a MIDI file, Melody.wav (the takes chosen per section, joined) and a WAV per take. Asks for a name only the first time, then saves over it.',
            'Save as: a copy under a new name; it suggests My Song v2, v3 …',
            'Recent projects: the last 10 are kept on the phone and open with one tap.'],
         'The MIDI file has Chords · Bass · Melody · Drums (when on) as separate tracks, ready to continue in a DAW.'),
    ]),
    ],
    notes=('Good to know', [
        'The app’s data lives in the browser’s storage. Clearing site data or uninstalling the browser can delete it, so back up with Save project.',
        'Record in the installed app or at its address; previews inside other apps may block the microphone. If the permission was refused, allow it again in the browser’s site settings.',
        'Bluetooth earphones add too much delay for recording; wired ones are recommended.',
        'Files are saved to Downloads as a .zip. Saving straight into a chosen folder is not supported yet.',
        'Some accompaniment styles and genre drums are 4/4 only; patterns approximate a genre’s feel.',
    ]),
)

CSS = r"""
*{box-sizing:border-box}
body{font-family:'Noto Sans CJK KR','Noto Sans KR','DejaVu Sans',sans-serif;color:#1b1f24;font-size:9.8pt;line-height:1.5;margin:0}
.cover{height:255mm;display:flex;flex-direction:column;justify-content:center;gap:6mm;break-after:page;background:linear-gradient(160deg,#101216,#1b1f26);color:#eceef1;border-radius:6mm;padding:0 16mm}
.cover h1{font-size:30pt;margin:0;letter-spacing:-.01em}
.cover h1 span{color:#34d3a6}
.cover p{font-size:12pt;color:#b9c0c9;margin:0;max-width:140mm}
.cover .ver{font:700 11pt 'DejaVu Sans Mono',monospace;color:#34d3a6}
.cover .row{display:flex;gap:5mm;margin-top:8mm;align-items:center;justify-content:center}
.cover .row img{width:42mm;border-radius:4mm;box-shadow:0 6mm 14mm rgba(0,0,0,.5)}
.cover .row img.mid{width:52mm}
.part{break-before:page;margin:0 0 6mm;padding:3mm 0 2mm;border-bottom:.6mm solid #34d3a6;font-size:11pt;font-weight:800;color:#1f8f70;letter-spacing:.04em}
h2{font-size:14.5pt;margin:0 0 1.5mm;display:flex;align-items:center;gap:3mm}
h2 i{font-style:normal;display:inline-grid;place-items:center;width:8mm;height:8mm;border-radius:2mm;background:#1b1f26;color:#34d3a6;font-size:11pt}
.sec{break-inside:avoid;margin:0 0 8mm}
.intro{color:#555d68;margin:0 0 3mm}
.body{display:flex;gap:7mm;align-items:flex-start}
.shots{display:flex;flex-direction:column;gap:4mm;flex:none}
.shot{position:relative;border-radius:3mm;box-shadow:0 1.2mm 4mm rgba(0,0,0,.25)}
.shot img{display:block;width:100%;height:100%;border-radius:3mm}
.mk{position:absolute;transform:translate(-50%,-50%);width:5.4mm;height:5.4mm;border-radius:50%;background:#ffcf33;color:#111;font:800 7.8pt/5.4mm 'DejaVu Sans',sans-serif;text-align:center;box-shadow:0 0 0 .5mm #111,0 .6mm 1.6mm rgba(0,0,0,.5)}
ol{margin:0;padding:0;list-style:none;counter-reset:n;flex:1}
ol li{counter-increment:n;position:relative;padding-left:7.5mm;margin:0 0 2.2mm}
ol li::before{content:counter(n);position:absolute;left:0;top:.2mm;width:5.4mm;height:5.4mm;border-radius:50%;background:#ffcf33;color:#111;font:800 7.8pt/5.4mm 'DejaVu Sans',sans-serif;text-align:center}
ol.plain li::before{content:'•';background:none;color:#34d3a6;font-size:12pt}
.tip{margin-top:3mm;padding:2.5mm 3.5mm;border-left:1mm solid #34d3a6;background:#eefaf6;border-radius:0 2mm 2mm 0;color:#244}
.start{break-after:page}
.toc{margin:4mm 0 0}
.toc h3{font-size:10pt;color:#1f8f70;margin:4mm 0 1mm}
.toc div{padding:1.1mm 0;border-bottom:.2mm solid #e3e6ea}
b{font-weight:700}
"""

def build(L):
    out = ['<!doctype html><html lang="%s"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>' % (L['lang'], L['title'], CSS)]
    t = L['title'].split(' ', 1)
    out.append('<section class="cover"><div class="ver">PhraseNote %s</div><h1><span>%s</span> %s</h1><p>%s</p><div class="row"><img src="img/main.png"><img class="mid" src="img/cover_roll.png"><img src="img/audio.png"></div></section>' % (
        VER, html.escape(t[0]), html.escape(t[1] if len(t) > 1 else ''), html.escape(L['sub'])))
    out.append('<section class="start"><h2><i>0</i>%s</h2><ol class="plain">%s</ol>' % (L['install'][0], ''.join('<li>%s</li>' % x for x in L['install'][1])))
    toc, n = [], 0
    for pt, secs in L['parts']:
        toc.append('<h3>%s</h3>' % pt)
        for s in secs:
            n += 1; toc.append('<div>%d · %s</div>' % (n, s[0]))
    toc.append('<h3>&nbsp;</h3><div>%d · %s</div>' % (n + 1, L['notes'][0]))
    out.append('<h2 style="margin-top:9mm">%s</h2><div class="toc">%s</div></section>' % (L['toc'], ''.join(toc)))
    n = 0
    for pt, secs in L['parts']:
        out.append('<div class="part">%s</div>' % pt)
        for title, intro, shots, items, tip in secs:
            n += 1
            imgs = ''.join(shot(nm, w) for nm, w in shots)
            out.append('<section class="sec"><h2><i>%d</i>%s</h2>%s<div class="body"><div class="shots">%s</div><div style="flex:1"><ol>%s</ol>%s</div></div></section>' % (
                n, title, ('<p class="intro">%s</p>' % intro) if intro else '', imgs,
                ''.join('<li>%s</li>' % x for x in items), ('<div class="tip">%s</div>' % tip) if tip else ''))
    out.append('<section class="sec"><h2><i>%d</i>%s</h2><ol class="plain">%s</ol></section>' % (n + 1, L['notes'][0], ''.join('<li>%s</li>' % x for x in L['notes'][1])))
    out.append('</body></html>')
    open(os.path.join(HERE, L['lang'] + '.html'), 'w').write('\n'.join(out))

for L in (KO, EN):
    build(L)
print('ok')
