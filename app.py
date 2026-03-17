import random
import pandas as pd
import streamlit as st
import aiohttp
import asyncio
from pokemon_api import pokemon_data,get_batsugun_tyeps,get_pokemon_types, make_choices_answer

st.set_page_config(page_title='ポケモン バツグン クイズ', layout='centered')

# ---------------
# 初期化
# ---------------
if 'started' not in st.session_state:
    st.session_state['started'] = False

if 'current_index' not in st.session_state:
    st.session_state['current_index'] = 0

if 'score' not in st.session_state:
    st.session_state['score'] = 0

if 'finished' not in st.session_state:
    st.session_state['finished'] = False

if 'answered' not in st.session_state:
    st.session_state['answered'] = False

if 'selected_choice' not in st.session_state:
    st.session_state['selected_choice'] = False

if 'is_correct' not in st.session_state:
    st.session_state['is_correct'] = False

if 'questions' not in st.session_state:
    st.session_state['questions'] = []

# ---------------
# 関数
# ---------------
def start_quiz():
    st.session_state.started = True
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.answered = False
    st.session_state.selected_choice = None
    st.session_state.is_correct = None
    st.session_state.questions = make_quiz()

def make_quiz():
    # 5件のポケモンを取得
    random_integers = [random.randint(1, 500) for _ in range(5)]
    questions = []
    for i in random_integers:
        pokemon = pokemon_data(i)
        choices, answer = make_choices_answer(pokemon['type'])
        questions.append({
            "name": pokemon['jp_name'],
            "image_url": pokemon['image_url'],
            "type": pokemon['type'],
            "question": "バツグンなのはどのタイプ？",
            "choices": choices,
            "answer": answer,
        })
    return questions

def make_choices_answer(type):
    batsugun = get_batsugun_tyeps(type)
    answer = random.sample(batsugun, 1)[0]
    types = get_pokemon_types()
    choices = list(set(batsugun) ^ set(types))
    if type in choices:
        choices.remove(type)
    choices = random.sample(choices, 3)
    choices.insert(random.randint(0,len(choices)), answer)
    return choices, answer

def answer_question(choice):
    q = st.session_state.questions[st.session_state.current_index]
    st.session_state.selected_choice = choice
    st.session_state.answered = True
    st.session_state.is_correct = (choice == q["answer"])

    if st.session_state.is_correct:
        st.session_state.score += 1

def next_question():
    st.session_state.current_index += 1
    st.session_state.answered = False
    st.session_state.selected_choice = None
    st.session_state.is_correct = None

    if st.session_state.current_index >= len(st.session_state.questions):
        st.session_state.finished = True
# ---------------
# 画面
# ---------------
with st.sidebar:
    st.header('メニュー')
    if st.button('スタート'):
        start_quiz()
        st.rerun()

    if st.button('最初からやり直す'):
        start_quiz()
        st.rerun()
    st.subheader('タイプ英語早見表')
    type_table = pd.DataFrame(
        {
            "英語":["normal", "fighting", "flying", "poison", "ground",
                    "rock", "bug", "ghost", "steel", "fire", "water",
                    "grass", "electric", "psychic", "ice", "dragon",
                    "dark", "fairy",],
            "日本語": ["ノーマル", "かくとう", "ひこう", "どく", "じめん", 
                    "いわ", "むし", "ゴースト", "はがね", "ほのお", "みず",
                    "くさ", "でんき", "エスパー", "こおり", "ドラゴン", 
                    "あく", "フェアリー",]
        },
    )
    st.dataframe(type_table, hide_index=True)

st.title('✨ポケモン バツグン クイズ✨')

if not st.session_state['started']:
    st.write('スタートボタンを押してください')
elif st.session_state['finished']:
    st.subheader('終了')
    st.write(f"得点：{st.session_state.score} / {len(st.session_state.questions)}")
    if st.session_state.score == 5:
        st.success('全問正解です！')
        st.balloons()
    elif st.session_state.score >= 3:
        st.success('よくできました！')
else:
    q = st.session_state.questions[st.session_state.current_index]
    st.write(f"**第 {st.session_state.current_index + 1} 問 / {len(st.session_state.questions)} 問**")
    st.subheader(q["question"])
    st.write(q['name'])
    st.write(q['type'])
    st.image(q['image_url'])

    if not st.session_state['answered']:
        for choice in q['choices']:
            if st.button(
                choice,
                key=f"choice_{st.session_state.current_index}_{choice}", 
                use_container_width=True
            ):
                answer_question(choice)
                st.rerun()
    else:
        st.write(f"あなたの回答：**{st.session_state.selected_choice}**")

        if st.session_state.is_correct:
            st.success("正解です")
        else:
            st.error(f"不正解です。正解は「{q['answer']}」です")

        if st.button("次へ", use_container_width=True):
            next_question()
            st.rerun()
