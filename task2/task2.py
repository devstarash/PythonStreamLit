import streamlit as st
import json
def get_question(file):
    try:
        with open(file,'r', encoding='utf-8') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        st.error(f"Файл {file} не найден!")
        return None
    except json.JSONDecodeError:
        st.error(f"Ошибка в формате JSON файла {file}!")
        return None
    except Exception as e:
        st.error(f"Ошибка загрузки файла: {e}")
        return None
st.title("📝 Тестовая система")
if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "test_completed" not in st.session_state:
    st.session_state["test_completed"] = False
if "test_selected" not in st.session_state:
    st.session_state["test_selected"] = False
if "selected_test_name" not in st.session_state:
    st.session_state["selected_test_name"] = ""
if not st.session_state["test_selected"]:
    st.subheader("Выберите тему теста:")
    test_options = [
        "Программирование",
        "География",
        "Литература",
        "Математика",
    ]
    selected_test = st.radio("", test_options)
    if st.button("Начать тест"):
        st.session_state["test_selected"] = True
        st.session_state["selected_test_name"] = selected_test
        st.session_state["current_question"] = 0
        st.session_state["score"] = 0
        st.session_state["test_completed"] = False
        st.rerun()
else:
    test_dictionary = {
        "Программирование": "python.json",
        "География": "geography.json",
        "Литература": "literature.json",
        "Математика": "math.json",

    }
    question_file = get_question(test_dictionary[st.session_state["selected_test_name"]])
    if question_file is None:
        st.stop()

    questions = question_file.get("questions",[])
    if len(questions) == 0:
        st.error("В файле нет вопросов или неправильный формат!")
        st.stop()
    if st.session_state["test_completed"]:
        st.write("🎉 Тест пройден!")
        st.write(f'Ваш результат {st.session_state["score"]}  из {len(questions)} ({(st.session_state["score"] / len(questions)) * 100:.0f}%)')
        if st.button("🔄 Пройти тест заново"):
            st.session_state["current_question"] = 0
            st.session_state["score"] = 0
            st.session_state["test_completed"] = False
            st.session_state["user_answers"] = []
            st.rerun()
        if st.button("📚 Сменить тему теста"):
            st.session_state["test_selected"] = False
            st.rerun()
    else:
        current_q = questions[st.session_state["current_question"]]
        st.subheader(f'Вопрос {st.session_state["current_question"] + 1} из {len(questions)}')
        if current_q["type"] == "single":
            answers = [answers["text"] for answers in current_q["answers"]]
            st.write(current_q["question"])
            selected = st.radio("Выберите правильный ответ", answers)
            if st.button("Отправить"):
                for answer in current_q["answers"]:
                    if answer["correct"] == True:
                        answers_correct = answer["text"]
                if answers_correct == selected:
                    st.session_state["score"] += 1
                if (st.session_state["current_question"] < len(questions) - 1):
                    st.session_state["current_question"] += 1
                else:
                    st.session_state["test_completed"] = True
                st.rerun()
        if current_q["type"] == "multiple":
            st.write(current_q["question"])
            st.write("Выберите правильные ответы:")
            for answer in current_q["answers"]:
                st.checkbox(answer["text"],key=f"q{st.session_state.current_question}_{answer['text']}")
            if st.button("Отправить"):
                result =[]
                c_result = []
                for answer in current_q["answers"]:
                    c_result.append(answer["correct"])
                    key = f"q{st.session_state.current_question}_{answer['text']}"
                    result_check_box = st.session_state.get(key, False)
                    result.append(result_check_box)
                if (result == c_result):
                    st.session_state["score"] += 1
                if(st.session_state["current_question"] < len(questions) - 1):
                    st.session_state["current_question"] += 1
                else:
                    st.session_state["test_completed"] = True
                st.rerun()









