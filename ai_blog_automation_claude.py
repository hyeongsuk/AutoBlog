"""
Claude AI 콘텐츠 생성 + 네이버 블로그 자동화 통합 프로그램
Anthropic Claude API로 콘텐츠를 생성하고 자동으로 블로그에 포스팅
"""

import os
import sys
from 블로그_글쓰기_자동화 import NaverBlogAutomation
from ai_content_generator_claude import ClaudeContentGenerator


def main():
    """Claude AI 콘텐츠 생성 + 블로그 자동화 메인 함수"""
    print("=" * 60)
    print("Claude AI 콘텐츠 생성 + 네이버 블로그 자동화 프로그램")
    print("=" * 60)
    print()

    # 모드 선택
    print("실행 모드를 선택하세요:")
    print("1. 수동 입력 (직접 제목과 본문 입력)")
    print("2. Claude AI 콘텐츠 생성 (키워드 입력 → AI가 제목과 본문 생성)")
    print("3. 엑셀 대량 생성 (엑셀 파일의 키워드로 여러 포스트 생성)")

    mode = input("\n선택 (1, 2, 3): ").strip()

    if mode == '1':
        # 수동 입력 모드
        print("\n=== 수동 입력 모드 ===")
        title = input("제목을 입력하세요: ").strip()

        print("\n본문을 입력하세요 (각 줄마다 Enter, 완료 후 빈 줄에서 Enter):")
        content_lines = []
        while True:
            line = input()
            if not line:
                break
            content_lines.append(line)

        if not title or not content_lines:
            print("제목과 본문을 모두 입력해주세요.")
            return

        # 블로그 자동화 실행
        automation = NaverBlogAutomation()
        automation.run(title, content_lines)

    elif mode == '2':
        # Claude AI 단일 키워드 모드
        print("\n=== Claude AI 콘텐츠 생성 모드 ===")
        keyword = input("블로그 포스트 키워드를 입력하세요: ").strip()

        if not keyword:
            print("키워드를 입력해주세요.")
            return

        try:
            # Claude AI 콘텐츠 생성
            print("\nClaude AI가 콘텐츠를 생성 중입니다...")
            generator = ClaudeContentGenerator()
            result = generator.generate_blog_post(keyword)

            title = result['title']
            content_lines = result['content']

            print(f"\n생성된 제목: {title}")
            print(f"생성된 본문: {len(content_lines)}개 문단")

            # 미리보기
            print("\n=== 생성된 콘텐츠 미리보기 ===")
            print(f"제목: {title}")
            print("\n본문:")
            for i, line in enumerate(content_lines[:3], 1):  # 처음 3문단만 표시
                print(f"{i}. {line}")
            if len(content_lines) > 3:
                print(f"... (총 {len(content_lines)}개 문단)")

            # 사용자 확인
            confirm = input("\n이 내용으로 블로그에 포스팅하시겠습니까? (y/n): ").strip().lower()

            if confirm == 'y':
                # 블로그 자동화 실행
                automation = NaverBlogAutomation()
                automation.run(title, content_lines)
            else:
                print("포스팅이 취소되었습니다.")

        except ValueError as e:
            print(f"\n오류: {str(e)}")
            print("CLAUDE_API_KEY를 .env 파일에 설정해주세요.")
            return

    elif mode == '3':
        # 엑셀 대량 생성 모드
        print("\n=== 엑셀 대량 생성 모드 ===")
        excel_file = input("엑셀 파일 경로를 입력하세요: ").strip()

        if not os.path.exists(excel_file):
            print("파일을 찾을 수 없습니다.")
            return

        try:
            # Claude AI 콘텐츠 대량 생성
            generator = ClaudeContentGenerator()
            results = generator.generate_from_excel(excel_file)

            if not results:
                print("생성된 콘텐츠가 없습니다.")
                return

            print(f"\n총 {len(results)}개의 포스트가 생성되었습니다.")
            print("\n각 포스트를 순차적으로 업로드하시겠습니까?")
            confirm = input("계속하려면 'y'를 입력하세요 (y/n): ").strip().lower()

            if confirm != 'y':
                print("업로드가 취소되었습니다.")
                return

            # 블로그 자동화 객체 생성
            automation = NaverBlogAutomation()

            # 각 포스트 순차 업로드
            for i, result in enumerate(results, 1):
                print(f"\n\n{'=' * 60}")
                print(f"[{i}/{len(results)}] 포스팅 중: {result['keyword']}")
                print('=' * 60)

                automation.run(result['title'], result['content'])

                # 다음 포스트 전에 대기
                if i < len(results):
                    print("\n다음 포스트로 이동하려면 Enter를 누르세요...")
                    input()

            print("\n모든 포스트 업로드 완료!")

        except ValueError as e:
            print(f"\n오류: {str(e)}")
            print("CLAUDE_API_KEY를 .env 파일에 설정해주세요.")
            return

    else:
        print("잘못된 선택입니다.")


if __name__ == "__main__":
    main()
