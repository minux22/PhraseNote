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
    sub='모바일(Android) 환경을 위한 코드 / 멜로디 스케치용 웹앱',
    toc='차례',
    about=('개요', [
        'PhraseNote는 떠오른 악상을 휴대폰에서 바로 기록하고 들어볼 수 있도록 만든 작곡 스케치용 웹앱입니다.',
        '앱은 <b>코드 트랙</b>과 <b>멜로디 트랙</b> 두 축으로 구성됩니다. 코드 트랙에서 곡의 화성 진행과 구조를 정하고, 멜로디 트랙에서 그 위에 선율을 입력하거나 노래로 녹음합니다.',
        '반주, 베이스, 드럼, 음량 강약 등 그 밖의 요소는 사용자가 세부를 일일이 다루지 않아도 되도록 자동화하거나 최소한의 설정으로 단순화하였습니다. 작업 결과는 MIDI와 WAV 파일로 저장되므로 DAW에서 이어서 편곡할 수 있습니다.',
    ], '주요 특징', [
        '<b>코드 진행 자동 생성</b> — 버튼 하나로 조와 스케일에 맞는 코드 진행을 무작위로 생성합니다.',
        '<b>멜로디 기반 코드 추천</b> — 멜로디를 먼저 입력한 경우, 선율에 어울리는 코드 진행을 제안하고 조를 추정합니다.',
        '<b>자동 반주</b> — 반주 스타일만 선택하면 코드에 맞는 반주 패턴과 베이스 라인이 생성됩니다.',
        '<b>Auto-Velocity</b> — 멜로디의 세기를 박의 위치에 따라 자동으로 조절하여 자연스러운 강약을 만듭니다.',
        '<b>장르별 드럼 패턴</b> — 다양한 장르의 드럼 패턴을 선택하거나 직접 편집할 수 있습니다.',
        '<b>Loop 기반 확장</b> — 한 구간을 반복하며 멜로디를 이어 쓰면 곡 구조가 자동으로 늘어납니다.',
        '<b>구간별 테이크 선택</b> — 노래를 여러 번 녹음한 뒤 섹션마다 가장 좋은 테이크를 골라 하나의 멜로디로 완성합니다.',
        '<b>MIDI · WAV 동시 저장</b> — 프로젝트를 저장하면 MIDI 파일과 오디오 파일이 함께 만들어집니다.',
    ]),
    install=('시작하기', [
        '<b>앱 주소</b> https://minux22.github.io/PhraseNote/',
        '<b>삼성 인터넷에서 설치</b> 앱 주소에 접속한 뒤 메뉴(☰) → 페이지 추가 → 홈 화면 → 추가를 선택합니다. 주소창에 설치 아이콘이 표시되면 해당 아이콘으로도 설치할 수 있습니다.',
        '<b>Chrome에서 설치</b> 앱 주소에 접속한 뒤 메뉴(⋮) → 앱 설치 또는 홈 화면에 추가를 선택합니다.',
        '설치한 앱은 홈 화면 아이콘으로 실행되며 전체 화면으로 표시됩니다. 최초 실행 후에는 인터넷 연결 없이도 사용할 수 있습니다.',
        '<b>업데이트</b> 새 버전이 배포되면 앱을 완전히 종료한 뒤 두 번 다시 실행하면 적용됩니다. 첫 실행에서 새 버전을 내려받고, 두 번째 실행에서 적용됩니다. 현재 버전은 화면 하단에 표시됩니다.',
        '<b>자동 보관</b> 작업 내용과 녹음은 편집할 때마다 기기 내부에 자동으로 보관됩니다. 백업하거나 다른 기기로 옮기려면 Setup의 Save project로 파일을 저장하십시오.',
        '<b>기본 작업 순서</b> 코드 트랙에서 코드 진행과 반주·드럼을 구성 → 멜로디 트랙에서 멜로디 입력 또는 노래 녹음 → 믹서에서 음량 균형 조정 → Save project로 저장.',
    ]),
    parts=[
    ('코드 트랙', [
        ('기본 화면', '화면 상단의 조작부는 코드 트랙과 멜로디 트랙에서 공통으로 사용됩니다.', [('main', 70)], [
            '재생 / 정지. 재생 위치(흰색 선)에서 재생을 시작합니다.',
            '처음으로. 재생 위치를 곡의 처음으로 이동합니다.',
            'BPM. − / + 버튼으로 1씩 조정하거나 숫자를 눌러 직접 입력합니다(40~200).',
            '드럼 켜기 / 끄기. 켜면 선택한 드럼 패턴이 함께 연주됩니다.',
            '드럼 패턴 목록을 엽니다(5장 참조).',
            '실행 취소 / 다시 실행. 코드, 멜로디, 곡 구조의 편집에 적용됩니다.',
            '박자, 조, 스케일. 조 목록 맨 위의 “Guess from melody…”는 멜로디로 조를 추정합니다(10장 참조).',
            '코드 트랙 / 멜로디 트랙 전환. 재생 중에 전환해도 재생은 계속됩니다.',
            '믹서를 엽니다(13장 참조).', 'Setup을 엽니다. 저장, 열기, 음원 설정을 다룹니다(14·15장 참조).'],
         '하단의 Keys, Mixer, Setup은 한 번에 하나만 열립니다. 다른 항목을 열면 기존 항목은 닫힙니다.'),
        ('곡 구조 (Song structure)', '곡은 섹션(A, B …)을 담은 슬롯을 순서대로 배열하여 구성합니다. 하나의 섹션을 여러 슬롯에서 반복하여 사용할 수 있습니다.', [('form', 70)], [
            '슬롯. 누르면 선택되며, 아래 코드 그리드에 해당 섹션이 표시됩니다. 길게 누른 상태로 좌우로 끌면 순서를 변경할 수 있습니다.',
            '+ (슬롯 추가). 새 섹션 생성, 기존 섹션 반복, 다른 프로젝트 파일에서 섹션 가져오기 중 하나를 선택합니다. 새 섹션은 현재 섹션과 같은 길이로 생성됩니다.',
            'Loop / Song. Loop는 선택한 슬롯만 반복 재생하고, Song은 곡 전체를 재생합니다. 멜로디 트랙에서의 Loop 동작은 12장을 참조하십시오.',
            'Edit. 선택한 슬롯의 섹션 변경, 역할 지정(Intro · Verse · Pre · Chorus · Bridge · Outro), 이동 · 복제 · 삭제를 수행합니다.'], None),
        ('코드 입력', '팔레트에서 코드를 선택한 뒤 그리드에 입력합니다. 그리드에는 현재 선택한 섹션이 표시됩니다.', [('chords', 70)], [
            '팔레트. 현재 조와 스케일의 다이어토닉 코드가 로마 숫자와 코드명으로 표시됩니다. 누르면 소리가 나며 선택되고, Erase는 지우기 도구입니다.',
            '그리드. 칸을 누르거나 끌어서 선택한 코드를 입력합니다. 입력된 칸을 다시 누르면 삭제됩니다.',
            'Cell. 한 칸의 길이(1마디 · 2박 · 1박)이며, 코드가 바뀔 수 있는 최소 단위입니다.',
            'Bars. 해당 섹션의 마디 수(2 · 4 · 8 · 16)입니다.',
            'Bass는 베이스 파트의 사용 여부, 7th는 모든 코드의 7화음 적용 여부를 정합니다.',
            '/– (슬래시 코드). 베이스로 사용할 스케일 음을 선택한 뒤 칸에 입력하면 해당 음이 베이스가 됩니다.',
            'Random. 조와 스케일에 맞는 코드 진행을 무작위로 생성합니다. 해당 슬롯에 멜로디가 있으면 Suggest 버튼으로 바뀌며, 멜로디에 어울리는 진행을 제안합니다(10장 참조).',
            'More chords. 스케일 밖의 코드(차용 화음, 세컨더리 도미넌트 등)를 표시합니다.'],
         '생성된 진행이 마음에 들지 않으면 실행 취소로 이전 상태로 되돌릴 수 있습니다.'),
        ('반주 (Accompaniment)', '코드를 연주하는 방식을 정합니다. 섹션마다 다르게 지정할 수 있습니다(예: Verse는 아르페지오, Chorus는 스트럼).', [('accomp', 62)], [
            '스타일. Classic · Modern · Jazz/Soul · Rock/Folk 그룹에서 선택합니다. 스타일을 선택하면 그에 맞게 아래 세부 설정도 함께 조정됩니다.',
            'Voicing · Color · Bass. 화음 배치(밀집 · 개방 · 확장 · 연결 우선), 텐션(add9 · sus · 6/9 · 9th), 베이스 리듬(근음 · 근음+5도 · 옥타브 · 킥 연동)을 정합니다.',
            'Strum · Late. 기타 스트럼처럼 음을 시차를 두고 연주하거나, 코드를 박보다 약간 늦게 연주합니다.',
            'Swing · Loose. 8분 / 16분 스윙을 적용하거나, 연주 타이밍에 약간의 불규칙성을 더합니다.'],
         '밑줄이 있는 항목명을 누르면 간단한 도움말이 표시됩니다. 일부 스타일은 4/4 박자에서만 동작합니다.'),
        ('드럼', '드럼 버튼 옆 화살표를 누르면 패턴 목록이 열립니다. 드럼 패턴도 섹션별로 지정됩니다.', [('drumlist', 52), ('drumgrid', 62)], [
            '목록에서 패턴을 누르면 미리 듣기와 함께 드럼이 켜집니다. 맨 아래의 My pattern을 누르면 사용자 패턴 편집 창이 열립니다.',
            '8th / 16th. 한 마디를 8칸 또는 16칸으로 나눕니다.',
            'Test. 반주 없이 드럼 패턴만 반복 재생합니다.',
            'From preset. 목록에서 마지막으로 선택한 패턴을 복사하여 편집을 시작합니다. Clear는 모든 칸을 지웁니다.',
            '악기별 줄(킥 · 스네어 · 사이드 스틱 · 하이햇 · 오픈 햇 · 라이드 · 클랩)의 칸을 눌러 켜고 끕니다. Done으로 창을 닫습니다.'], None),
    ]),
    ('멜로디 트랙', [
        ('피아노롤 (Roll)', '멜로디 트랙의 기본 편집 화면입니다. 상단의 코드 줄에 코드 트랙의 진행이 표시됩니다.', [('roll', 70)], [
            'Mode. Roll(피아노롤) · Staff(오선보) · Audio(노래 녹음)를 전환합니다. 재생 중에도 전환할 수 있습니다.',
            'Pickup. 곡 앞에 못갖춘마디를 추가합니다.',
            'Auto-Velocity. 멜로디의 세기를 박의 위치에 따라 자동으로 조절합니다(0% = 균일, 100% = 최대).',
            '도구. 펜: 빈 곳을 누르면 음 입력, 끌면 길이와 음높이 조정, 음을 누르면 삭제. 선택: 영역을 지정하여 복사 · 붙여넣기 · 이동 · 옥타브 이동 · 삭제. 손: 편집 없이 화면 이동.',
            'Len · Snap. 새로 입력할 음의 길이와, 음이 맞춰지는 박 단위를 지정합니다.',
            '코드 줄. 마디별 코드와 섹션 이름이 표시됩니다. 오른쪽 아래 − / + 버튼으로 가로 배율을 조정합니다.'], None),
        ('오선보 (Staff)', '같은 멜로디를 악보 형태로 표시하고 편집합니다.', [('staff', 70)], [
            '도구. 펜 · 선택 · 손(피아노롤과 동일).',
            '음표 길이. 온음표부터 16분음표까지 선택한 뒤 오선을 누릅니다.',
            '점음표. 선택한 음표의 길이를 1.5배로 합니다.',
            '임시표. ♯ · ♭ · ♮를 붙여 입력합니다.'],
         '오선을 누른 상태로 위아래로 끌면 음높이를 들으며 선택할 수 있으며, 손을 떼면 입력됩니다. 선택 도구로 고른 음은 ▲▼(반음) · ◀▶(16분음표) 버튼으로 이동합니다.'),
        ('건반 입력 (Keys)', '하단의 Keys를 누르면 화면 건반이 열립니다. Roll과 Staff 모드에서 사용할 수 있습니다.', [('keys', 64)], [
            'Live / Step. Live는 연주를 실시간으로 녹음하고, Step은 건반을 누를 때마다 한 음씩 순서대로 입력합니다(음 길이는 Len 설정을 따름).',
            'Rec. 활성화한 뒤 재생하면 1마디 카운트인 후 녹음이 시작됩니다. 카운트인은 Count-in으로 끌 수 있습니다.',
            'Quant. 녹음된 음을 지정한 박 단위(16 · 8 · 4분)에 맞춥니다.',
            'Latency. 기기의 오디오 지연을 측정하여 녹음 타이밍을 보정합니다. 처음 한 번 측정하는 것을 권장합니다.',
            '◀ ▶. 건반의 음역을 이동합니다.'], None),
        ('퀀타이즈 (Quantize)', '입력된 모든 음의 타이밍을 정리합니다. 멜로디 편집 화면 하단의 Quantize를 열어 사용합니다.', [('quant', 62)], [
            'Grid. 맞출 박 단위(32분 ~ 4분, 셋잇단 16T · 8T)를 선택합니다.',
            'Strength. 보정 강도입니다(100% = 박에 정확히 맞춤, 50% = 절반만 보정).',
            'Quantize all notes. 퀀타이즈를 실행합니다. Length를 켜면 음 길이도 함께 보정합니다.'], None),
        ('멜로디 기반 조 추정 · 코드 추천', '멜로디를 먼저 작성한 경우, 멜로디에 맞는 조와 코드 진행을 제안받을 수 있습니다.', [('keyguess', 56), ('suggest', 62)], [
            '조 추정. 조 목록 맨 위의 “Guess from melody…”를 선택하면 가능성이 높은 조 3개가 표시됩니다. Apply는 조 이름만 변경하며 멜로디와 코드의 실제 소리는 바뀌지 않습니다.',
            'Suggest. 멜로디가 있는 슬롯에서는 코드 트랙의 Random 버튼이 Suggest로 바뀝니다. 누르면 멜로디에 어울리는 코드로 빈칸을 채우며, 다시 누를 때마다 다른 제안(최대 5개)이 표시됩니다.'], None),
        ('노래 녹음 (Audio)', 'Mode에서 Audio를 선택하면 반주를 들으며 마이크로 녹음할 수 있습니다. 반주가 녹음에 섞이지 않도록 유선 이어폰 사용을 권장합니다.', [('audio', 72)], [
            'Mode에서 Audio를 선택합니다. 마이크는 이 모드에서만 활성화됩니다.',
            '입력 장치. 일반적으로 기본값을 그대로 사용합니다.',
            'Calibrate. 처음 한 번, 이어폰을 뺀 상태에서 음량을 높이고 실행합니다. 스피커의 클릭음을 마이크로 다시 받아 지연 시간을 측정하고 녹음 위치를 보정합니다.',
            'Input. 마이크 입력 증폭입니다. 가장 크게 부르는 부분에서 아래 미터가 주황색 부근까지 오도록 조정하고, 수치가 빨간색으로 바뀌면 낮춥니다.',
            'Loop / Song. Loop는 지정한 마디 구간을 반복하며 한 바퀴마다 테이크를 하나씩 저장하고, Song은 재생 위치부터 Stop을 누를 때까지 한 번에 녹음합니다.',
            '반복 구간. Loop일 때 시작 마디와 끝 마디(끝 마디 포함)를 지정합니다. 재생 시에도 이 구간이 반복되며, 구간 밖은 어둡게 표시됩니다.',
            'REC. 반주 1마디가 재생된 뒤 녹음이 시작됩니다. 다시 누르면 녹음이 종료되고 테이크가 저장됩니다.',
            '타임라인. 섹션을 누르면 해당 섹션이 선택되고 재생 위치도 이동합니다. 섹션별로 선택한 테이크가 각 위치에 표시되며 함께 재생됩니다.',
            '선택한 섹션의 테이크 목록. 행을 누르면 해당 테이크를 이 섹션에 사용하며, 다시 누르면 해제됩니다. ▶ 해당 섹션부터 재생 · WAV 내보내기 · ✕ 삭제(실행 취소 가능).'],
         '테이크 이름은 Song-Bar01-1st, Loop-Bar01-04-2nd와 같이 시작 마디와 순번으로 지정됩니다. 녹음 중 MIDI 멜로디를 듣지 않으려면 믹서에서 MIDI 채널을 뮤트하십시오.'),
        ('Loop 기반 확장', '코드 트랙이 Loop 상태이면 멜로디 트랙에서도 선택한 슬롯이 반복됩니다. 이 상태에서 멜로디를 이어 쓰면 곡 구조가 자동으로 확장됩니다.', [('ghost', 70)], [
            '마지막 슬롯을 선택하면 곡 끝에 해당 슬롯의 복사본이 점선으로 표시됩니다. 이 영역에 음을 입력하면 실제 슬롯으로 추가되고, 그 뒤에 새 점선 영역이 다시 표시됩니다.',
            '녹음(노래 또는 Keys의 Live)은 슬롯 끝에서 처음으로 돌아가지 않고, 다음 복사본을 미리 생성하면서 계속 진행됩니다.',
            '중간 슬롯을 Loop로 지정한 경우 복사본은 해당 슬롯 바로 뒤에 삽입되며, 이후 섹션과 그 멜로디는 그만큼 뒤로 이동합니다.',
            'Keys 녹음 후 음이 없는 복사본은 녹음 종료 시 삭제됩니다. 노래 녹음은 녹음이 진행된 구간까지의 복사본이 유지됩니다.'], None),
    ]),
    ('음향과 저장', [
        ('믹서', '하단의 Mixer를 누르면 열립니다. 파트별 음량과 뮤트 · 솔로를 조정하며, 설정은 프로젝트에 함께 저장됩니다.', [('mixer', 72)], [
            '채널 구성. Melody MIDI(입력한 멜로디) · Melody Audio(녹음한 노래) · Chords · Bass · Drums.',
            '페이더. 위아래로 끌어 음량을 조정합니다. 기본값은 0.0 dB이며 최대 +12 dB입니다. 두 번 누르면 기본값으로 돌아갑니다. 눈금을 지날 때마다 짧은 진동이 발생합니다.',
            'M(뮤트). 해당 채널의 소리를 끕니다.',
            'S(솔로). 솔로를 켠 채널만 재생됩니다. 여러 채널을 동시에 솔로로 지정할 수 있습니다.',
            'Rev. 리버브의 양입니다(SoundFont 음원에 적용).',
            'Master. 전체 음량입니다.',
            '레벨 미터. 실제 출력 레벨을 표시합니다. 노란색 구간 이내가 적정하며, 상단의 빨간색이 자주 켜지면 Master를 낮추십시오. 하단 수치는 최근 최대 레벨입니다.'],
         '저장되는 MIDI 파일에는 각 트랙의 페이더 값이 볼륨 정보로 기록됩니다.'),
        ('음원 (SoundFont)', 'Setup의 Sound에서 악기 음원을 선택합니다.', [('setup_sound', 66)], [
            'Basic Synth는 별도 파일 없이 동작하는 기본 음원이며, SoundFont는 실제 악기 샘플을 사용하는 음원입니다.',
            'Load SoundFont. .sf2 파일(예: GeneralUser GS)을 불러오면 Melody · Chords · Bass · Drums 트랙별로 악기를 선택할 수 있습니다. 불러온 파일은 기기에 보관됩니다. 이후 Save / Load preset으로 악기 구성과 믹서 설정을 함께 저장하고 불러올 수 있습니다.',
            '드럼 패턴 선택과 편집(5장의 편집 창).'], None),
        ('저장과 열기', 'Setup의 Project에서 수행합니다.', [('setup_project', 66)], [
            'New project. 새 프로젝트를 시작합니다(두 번 눌러 확인).',
            'Open project. 저장한 .zip 또는 .phrasenote 파일을 엽니다. 녹음도 함께 복원됩니다.',
            'Save project. 다운로드 폴더에 .zip 파일 하나로 저장합니다. 이 파일에는 프로젝트 파일, MIDI 파일, Melody.wav(섹션별로 선택한 테이크를 합친 멜로디 오디오), 테이크별 WAV 파일이 포함됩니다. 이름은 최초 저장 시에만 입력하며, 이후에는 같은 이름으로 덮어씁니다.',
            'Save as. 현재 내용을 다른 이름으로 저장합니다. 기본 이름은 My Song v2, v3 …와 같이 제안됩니다.',
            'Recent projects. 최근 작업한 프로젝트 10개가 기기에 보관되며 바로 열 수 있습니다.'],
         'MIDI 파일은 Chords · Bass · Melody · Drums(드럼 사용 시)가 트랙별로 분리되어 있어 DAW에서 바로 이어서 작업할 수 있습니다.'),
    ]),
    ],
    notes=('참고 사항', [
        '앱의 데이터는 브라우저 저장 공간에 보관됩니다. 사이트 데이터를 삭제하거나 브라우저를 제거하면 데이터가 삭제될 수 있으므로 Save project로 정기적으로 백업하십시오.',
        '녹음은 설치한 앱 또는 앱 주소에서 진행하십시오. 다른 앱의 미리보기 화면에서는 마이크 사용이 제한될 수 있습니다. 마이크 권한을 거부한 경우 브라우저의 사이트 설정에서 다시 허용하십시오.',
        '블루투스 이어폰은 지연이 커서 녹음에 적합하지 않습니다. 유선 이어폰 사용을 권장합니다.',
        '저장 파일은 다운로드 폴더에 .zip 형식으로 저장됩니다. 지정한 폴더에 직접 저장하는 기능은 현재 지원하지 않습니다.',
        '일부 반주 스타일과 장르별 드럼 패턴은 4/4 박자 전용이며, 각 패턴은 해당 장르의 특징을 근사적으로 재현한 것입니다.',
    ]),
)

EN = dict(
    lang='en', title='PhraseNote User Guide',
    sub='A chord and melody sketching web app for mobile (Android)',
    about=('Overview', [
        'PhraseNote is a composition sketch web app for capturing musical ideas on a phone and hearing them right away.',
        'It is built around two axes: the <b>Chord Track</b>, where you set the harmony and structure of the song, and the <b>Melody Track</b>, where you write a melody over it or record it by singing.',
        'Everything else — accompaniment, bass, drums, dynamics — is automated or reduced to a few settings, so you do not have to handle the details. Results are saved as MIDI and WAV files to continue in a DAW.',
    ], 'Key features', [
        '<b>Random progressions</b> — one tap generates a chord progression that fits the key and scale.',
        '<b>Chords from the melody</b> — written the melody first? The app suggests fitting chords and estimates the key.',
        '<b>Automatic accompaniment</b> — pick a style and the accompaniment pattern and bass line follow the chords.',
        '<b>Auto-Velocity</b> — melody dynamics follow the beat automatically for a natural feel.',
        '<b>Genre drum patterns</b> — choose from many genres or edit your own.',
        '<b>Loop-based growth</b> — keep writing over a looping section and the song structure extends itself.',
        '<b>Take selection per section</b> — record several takes and pick the best one for each section to make one melody.',
        '<b>MIDI and WAV together</b> — saving a project also writes the MIDI and audio files.',
    ]),
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
    notes=('Notes', [
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
.cover .row img{width:46mm;border-radius:4mm;box-shadow:0 6mm 14mm rgba(0,0,0,.5)}
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
.about p{margin:0 0 3.5mm;font-size:10.4pt;line-height:1.7}
.feat li{margin-bottom:3mm}
b{font-weight:700}
"""

def build(L):
    out = ['<!doctype html><html lang="%s"><head><meta charset="utf-8"><title>%s</title><style>%s</style></head><body>' % (L['lang'], L['title'], CSS)]
    t = L['title'].split(' ', 1)
    out.append('<section class="cover"><div class="ver">PhraseNote %s</div><h1><span>%s</span> %s</h1><p>%s</p><div class="row"><img src="img/main.png"><img src="img/cover_roll.png"><img src="img/cover_audio.png"></div></section>' % (
        VER, html.escape(t[0]), html.escape(t[1] if len(t) > 1 else ''), html.escape(L['sub'])))
    a = L['about']
    out.append('<section class="start about"><h2>%s</h2>%s<h2 style="margin-top:8mm">%s</h2><ol class="plain feat">%s</ol></section>' % (
        a[0], ''.join('<p>%s</p>' % x for x in a[1]), a[2], ''.join('<li>%s</li>' % x for x in a[3])))
    out.append('<section class="start"><h2>%s</h2><ol class="plain">%s</ol>' % (L['install'][0], ''.join('<li>%s</li>' % x for x in L['install'][1])))
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
