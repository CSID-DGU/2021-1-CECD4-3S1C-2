# Comment Analyser (댓글 분석기)

keras 라이브러리를 이용.
konlpy를 이용한 한국말 형태소 분석.

145393개의 네이버 댓글 샘플들을 활용하여, 학습 시킨 모델(comment_model.h5)을 미리 저장해둔 tokenizer word_index(wordIndex.json)와 함께 사용하여 앞으로 올 댓글을 sentiment_predict() 함수에 parameter로 넣으면 predict하여 결과값을 냄.