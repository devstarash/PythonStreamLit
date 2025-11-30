import streamlit as st
import json
st.title("Анкета о предпочтениях в отдыхе")
if "success" not in st.session_state:
    st.session_state["success"] = False
if "form_key" not in st.session_state:
    st.session_state["form_key"] = 0
if st.session_state["success"]:
    st.success("Форма успешно отправлена!")
    st.session_state["success"] = False
key = f'Questionnaire_number_{st.session_state["form_key"]}'
with st.form(key = key):
    user_name = st.text_input("Ваше Имя")
    type_of_holidays = st.radio("Какой тип отдыха Вы предпочитаете?",('Пляжный отдых', 'Активный туризм (горы, походы)', 'Экскурсионный (города, музеи)', 'Спокойный загородный отдых'), index =None)
    objects = st.multiselect("2. Какие природные объекты обязательно должны быть в вашем путешествии?",
        ['Горы', 'Океан / Море', 'Леса / Заповедники', 'Пустыня', 'Нет предпочтений'])

    slider = st.slider('Как вы видите баланс своего отдыха (от 1 — только расслабление на пляже до 10 — только посещение музеев и экскурсии)?',
                       min_value = 1,
                       max_value = 10,
                       step = 1, value = 5)

    without_the_internet = st.checkbox("Готовы ли вы провести более 3 дней без доступа к Интернету?")

    unusual_place = st.text_area("В каком самом необычном месте вы бывали?")

    submit_button = st.form_submit_button("Отправить")
    if submit_button:
        errors = []
        if user_name == "":
            errors.append("Введите ваше имя")
        if type_of_holidays is None:
            errors.append("Выберите предпочитаемый отдых")
        if len(objects) == 0:
            errors.append("Выберите хотя бы 1 объект")
        if unusual_place == "":
            errors.append(" Опишите самое необычное место")
        if len(errors) > 0:
           for error in errors:
               st.error(error)

        else:
            dictionary = {
            "user_name": user_name,
            "type_of_holidays": type_of_holidays,
            "objects": objects,
            "slider_key": slider,
            "without_the_internet": without_the_internet,
            "unusual_place": unusual_place,
            }
            with open("result.jsonl", "a") as file:
                result = json.dumps(dictionary, ensure_ascii=False)
                file.write(result + '\n')
            st.session_state["success"]  = True
            st.session_state["form_key"] += 1
            st.rerun()






