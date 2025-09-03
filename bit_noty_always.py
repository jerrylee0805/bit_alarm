import requests
import time
import os
import smtplib
from datetime import datetime
from dotenv import load_dotenv
from email.mime.text import MIMEText

# .env 파일 로드
load_dotenv()

# 설정
period = 5  # 실행 주기 (초)
api_key = os.getenv('TWELVE_DATA_API_KEY', 'demo')

# Gmail 설정
EMAIL_USER = os.getenv('EMAIL_USER')  # 발신자 Gmail
EMAIL_PASS = os.getenv('EMAIL_PASS')  # Gmail 앱 비밀번호
EMAIL_TO = os.getenv('EMAIL_TO')      # 수신자 이메일

url = "https://api.twelvedata.com/rsi"
params = {
    'symbol': 'BTC/USD',
    'interval': '1day',
    'time_period': 14,
    'apikey': api_key
}

def get_rsi():
    """RSI 조회 함수"""
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if "values" in data and len(data["values"]) > 0:
            rsi = float(data["values"][0]["rsi"])
            return rsi
        else:
            return None
    except:
        return None

def send_test_email(rsi):
    """테스트용 이메일 발송 (모든 RSI 값에 대해)"""
    if not all([EMAIL_USER, EMAIL_PASS, EMAIL_TO]):
        print("⚠️ 이메일 설정 필요: EMAIL_USER, EMAIL_PASS, EMAIL_TO")
        return False
    
    try:
        # 간단한 이메일 내용
        subject = f"Bitcoin RSI: {rsi:.2f}"
        body = f"""
현재 시간: {datetime.now().strftime('%H:%M:%S')}
Bitcoin RSI: {rsi:.2f}

테스트 알림입니다.
        """
        
        # 이메일 메시지 생성
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = EMAIL_USER
        msg['To'] = EMAIL_TO
        
        # Gmail SMTP로 발송
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        
        return True
        
    except Exception as e:
        print(f"❌ 이메일 발송 실패: {e}")
        return False

# 주기적 실행
print(f"🚀 Bitcoin RSI 테스트 알림 시작 (주기: {period}초)")
print("모든 RSI 값에 대해 이메일을 보냅니다 (테스트용)")
print("종료하려면 Ctrl+C를 누르세요")
print("-" * 50)

while True:
    current_time = datetime.now().strftime("%H:%M:%S")
    rsi = get_rsi()
    
    if rsi:
        # 이메일 발송 시도
        if send_test_email(rsi):
            print(f"[{current_time}] RSI: {rsi:.2f} | 📧 이메일 발송 완료!")
        else:
            print(f"[{current_time}] RSI: {rsi:.2f} | ❌ 이메일 발송 실패")
    else:
        print(f"[{current_time}] RSI 데이터 없음")
    
    time.sleep(period)