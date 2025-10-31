"""
네이버 블로그 자동화 글쓰기 프로그램
Selenium을 활용한 네이버 블로그 자동 포스팅
"""

import time
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

class NaverBlogAutomation:
    def __init__(self):
        """네이버 블로그 자동화 클래스 초기화"""
        self.naver_id = os.getenv('NAVER_ID')
        self.naver_pw = os.getenv('NAVER_PW')

        if not self.naver_id or not self.naver_pw:
            raise ValueError("환경 변수에 NAVER_ID와 NAVER_PW를 설정해주세요.")

        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Selenium WebDriver 설정"""
        print("브라우저 초기화 중...")

        chrome_options = Options()
        # 자동화 탐지 방지 옵션
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # User-Agent 설정 (봇 탐지 방지)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        # 창 크기 설정
        chrome_options.add_argument("--start-maximized")

        # WebDriver 생성
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # WebDriverWait 설정 (최대 20초 대기)
        self.wait = WebDriverWait(self.driver, 20)

        print("브라우저 초기화 완료")

    def login_naver(self):
        """네이버 로그인 (보안 우회 방식 적용)"""
        print("네이버 로그인 시도 중...")

        try:
            # 네이버 로그인 페이지 접속
            self.driver.get("https://nid.naver.com/nidlogin.login")
            time.sleep(2)

            # 아이디 입력란 찾기
            id_input = self.wait.until(
                EC.presence_of_element_located((By.ID, "id"))
            )

            # pyperclip을 사용한 아이디 입력 (보안 우회)
            id_input.click()
            time.sleep(0.5)
            pyperclip.copy(self.naver_id)
            id_input.send_keys(Keys.CONTROL, 'v')
            time.sleep(0.5)

            print("아이디 입력 완료")

            # 비밀번호 입력란 찾기
            pw_input = self.driver.find_element(By.ID, "pw")
            pw_input.click()
            time.sleep(0.5)

            # pyperclip을 사용한 비밀번호 입력 (보안 우회)
            pyperclip.copy(self.naver_pw)
            pw_input.send_keys(Keys.CONTROL, 'v')
            time.sleep(0.5)

            print("비밀번호 입력 완료")

            # 로그인 버튼 클릭
            login_btn = self.driver.find_element(By.ID, "log.login")
            login_btn.click()

            print("로그인 버튼 클릭 완료")

            # 로그인 완료 대기
            time.sleep(3)

            # 로그인 성공 여부 확인
            if "nid.naver.com" not in self.driver.current_url:
                print("로그인 성공!")
                return True
            else:
                print("로그인 실패 또는 추가 인증 필요")
                return False

        except Exception as e:
            print(f"로그인 중 오류 발생: {str(e)}")
            return False

    def go_to_blog_write(self):
        """블로그 글쓰기 페이지로 이동"""
        print("블로그 글쓰기 페이지로 이동 중...")

        try:
            # 블로그 글쓰기 페이지로 이동
            self.driver.get("https://blog.naver.com/")
            time.sleep(2)

            # 글쓰기 버튼 찾기 및 클릭
            write_btn = self.wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn_post"))
            )
            write_btn.click()

            time.sleep(3)
            print("글쓰기 페이지 접근 완료")

            return True

        except Exception as e:
            print(f"글쓰기 페이지 이동 중 오류: {str(e)}")
            # 직접 URL로 이동 시도
            try:
                self.driver.get("https://blog.naver.com/BlogPost.naver?blogId=")
                time.sleep(3)
                return True
            except:
                return False

    def switch_to_editor_frame(self):
        """에디터 iframe으로 전환"""
        print("에디터 프레임으로 전환 중...")

        try:
            # mainFrame으로 전환
            self.wait.until(
                EC.frame_to_be_available_and_switch_to_it((By.ID, "mainFrame"))
            )
            print("mainFrame 전환 완료")
            time.sleep(1)
            return True

        except Exception as e:
            print(f"프레임 전환 중 오류: {str(e)}")
            return False

    def close_popups(self):
        """팝업 닫기"""
        print("팝업 확인 및 닫기...")

        try:
            # 임시저장 글 팝업 닫기
            try:
                close_btn = self.driver.find_element(By.CSS_SELECTOR, "button.btn_close")
                close_btn.click()
                print("임시저장 팝업 닫기 완료")
                time.sleep(1)
            except NoSuchElementException:
                print("임시저장 팝업 없음")

            # 도움말 팝업 닫기
            try:
                help_close_btn = self.driver.find_element(By.CSS_SELECTOR, "button.se_popup_btn_close")
                help_close_btn.click()
                print("도움말 팝업 닫기 완료")
                time.sleep(1)
            except NoSuchElementException:
                print("도움말 팝업 없음")

        except Exception as e:
            print(f"팝업 닫기 중 오류: {str(e)}")

    def write_title(self, title):
        """제목 입력"""
        print(f"제목 입력 중: {title}")

        try:
            # 제목 입력란 찾기 (여러 셀렉터 시도)
            selectors = [
                "div.se_textarea",
                "textarea.se_textarea",
                "div.se-module-title",
                "textarea[placeholder*='제목']",
                "#subject"
            ]

            title_input = None
            for selector in selectors:
                try:
                    title_input = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if not title_input:
                print("제목 입력란을 찾을 수 없습니다.")
                return False

            # 제목 입력
            title_input.click()
            time.sleep(0.5)
            title_input.send_keys(title)

            print("제목 입력 완료")
            return True

        except Exception as e:
            print(f"제목 입력 중 오류: {str(e)}")
            return False

    def write_content(self, content_lines):
        """본문 내용 입력 (ActionChains로 타이핑 모방)"""
        print("본문 내용 입력 중...")

        try:
            # 본문 입력란 찾기
            selectors = [
                "div.se-component-content",
                "div.se_section_text",
                "div[contenteditable='true']",
                "iframe.se-module-text"
            ]

            content_input = None
            for selector in selectors:
                try:
                    content_input = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if not content_input:
                print("본문 입력란을 찾을 수 없습니다.")
                return False

            # 본문 영역 클릭
            content_input.click()
            time.sleep(0.5)

            # ActionChains를 사용하여 자연스러운 타이핑 구현
            actions = ActionChains(self.driver)

            for i, line in enumerate(content_lines):
                print(f"  {i+1}번째 줄 입력 중...")

                # 한 글자씩 입력 (0.01초 간격)
                for char in line:
                    actions.send_keys(char)
                    actions.pause(0.01)

                # 줄바꿈 (마지막 줄 제외)
                if i < len(content_lines) - 1:
                    actions.send_keys(Keys.ENTER)
                    actions.pause(0.1)

            # 모든 액션 실행
            actions.perform()

            print("본문 입력 완료")
            return True

        except Exception as e:
            print(f"본문 입력 중 오류: {str(e)}")
            return False

    def save_temp(self):
        """임시 저장"""
        print("임시 저장 중...")

        try:
            # iframe에서 나가기
            self.driver.switch_to.default_content()
            time.sleep(0.5)

            # 임시 저장 버튼 찾기
            selectors = [
                "button.save_btn",
                "button.save_BTN_bzc",
                "button[data-action='temp']",
                "a.btn_save"
            ]

            save_btn = None
            for selector in selectors:
                try:
                    save_btn = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue

            if not save_btn:
                print("임시 저장 버튼을 찾을 수 없습니다.")
                return False

            # 임시 저장 버튼 클릭
            save_btn.click()
            time.sleep(2)

            # 저장 완료 메시지 확인
            try:
                success_msg = self.driver.find_element(By.CSS_SELECTOR, "div.message, div.alert")
                print(f"저장 결과: {success_msg.text}")
            except:
                print("임시 저장 완료 (메시지 확인 불가)")

            return True

        except Exception as e:
            print(f"임시 저장 중 오류: {str(e)}")
            return False

    def run(self, title, content_lines):
        """전체 프로세스 실행"""
        try:
            # 1. 드라이버 설정
            self.setup_driver()

            # 2. 로그인
            if not self.login_naver():
                print("로그인 실패. 프로그램 종료")
                return False

            # 3. 글쓰기 페이지 이동
            if not self.go_to_blog_write():
                print("글쓰기 페이지 이동 실패")
                return False

            # 4. 에디터 프레임 전환
            if not self.switch_to_editor_frame():
                print("에디터 프레임 전환 실패")
                return False

            # 5. 팝업 닫기
            self.close_popups()

            # 6. 제목 입력
            if not self.write_title(title):
                print("제목 입력 실패")
                return False

            # 7. 본문 입력
            if not self.write_content(content_lines):
                print("본문 입력 실패")
                return False

            # 8. 임시 저장
            if not self.save_temp():
                print("임시 저장 실패")
                return False

            print("\n=== 모든 작업 완료 ===")
            print("브라우저를 열어두고 결과를 확인하세요.")
            print("종료하려면 Ctrl+C를 누르세요.")

            # 브라우저 유지 (사용자가 결과 확인할 수 있도록)
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n프로그램 종료")

            return True

        except Exception as e:
            print(f"실행 중 오류 발생: {str(e)}")
            return False

        finally:
            if self.driver:
                self.driver.quit()


def main():
    """메인 함수"""
    print("=" * 50)
    print("네이버 블로그 자동화 글쓰기 프로그램")
    print("=" * 50)
    print()

    # 테스트용 제목과 본문
    title = "[자동화] 자동화 프로그램 테스트 제목"
    content_lines = [
        "안녕하세요. 내용을 입력하고 있습니다. (1)",
        "안녕하세요. 내용을 입력하고 있습니다. (2)",
        "안녕하세요. 내용을 입력하고 있습니다. (3)",
        "안녕하세요. 내용을 입력하고 있습니다. (4)",
        "안녕하세요. 내용을 입력하고 있습니다. (5)"
    ]

    # 자동화 실행
    automation = NaverBlogAutomation()
    automation.run(title, content_lines)


if __name__ == "__main__":
    main()
