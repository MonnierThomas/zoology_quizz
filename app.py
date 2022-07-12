import glob
import random

import pandas as pd
import streamlit as st


def read_animals(path):
    return pd.read_csv(path, delimiter="\t", header=None).squeeze().to_dict()


def upload_picture(id):
    paths = glob.glob("pictures/*")
    paths_picture = []
    for path in paths:
        if (
            path[9:12] == f"{id}_"
            or path[9:12] == f"{id}."
            or path[9:11] == f"{id}."
            or path[9:11] == f"{id}_"
        ):
            paths_picture.append(path)
    return random.choice(paths_picture)


def show_image(path_picture):
    st.image(path_picture)


def random_id(n):
    return random.randint(0, n)


def check(answer, name):
    if answer.lower() == name.lower():
        st.success("True")
        return True
    else:
        st.error(f"Wrong, the answer was {name}")
        return False


def solo_quizz(data):
    st.markdown("## Guess the animal!")
    st.session_state["reload"] = False
    id = random_id(len(data))
    st.session_state["name"] = data[id]
    st.session_state["path_picture"] = upload_picture(id + 1)
    show_image(st.session_state["path_picture"])
    st.session_state["answer"] = st.text_input(
        "Name of the animal: ",
        on_change=reload
    )


def display_grade():
    grade = st.session_state["res"] / st.session_state["n"]
    if grade > 10.0:
        st.success(
            f"Congrats, your grade is {grade} / {st.session_state['n']}"
        )
    else:
        st.error(f"Careful, your grade is {grade}")


def reload():
    st.session_state["reload"] = True


def full_reload():
    st.session_state["started"] = False


if __name__ == "__main__":
    if "started" not in st.session_state:
        st.session_state["started"] = False

    if "n" not in st.session_state or not st.session_state["started"]:
        st.title('Will you succeed the exam? Let"s see...')
        st.session_state["n"] = st.slider(
            "Choose the number of images you want", 5, 30, step=5
        )
        st.session_state["k"] = st.session_state["n"]

    if "data" not in st.session_state:
        st.session_state["data"] = read_animals("names.txt")

    if "res" not in st.session_state:
        st.session_state["res"] = 0

    if not st.session_state["started"]:
        go = st.button("Launch the test")
        if go:
            st.session_state["started"] = True
            st.session_state["reload"] = False
            if st.session_state["n"] > 1:
                solo_quizz(st.session_state["data"])

    if st.session_state["started"] and st.session_state["reload"]:
        show_image(st.session_state["path_picture"])
        res_bool = check(st.session_state["answer"], st.session_state["name"])
        st.session_state["res"] += int(res_bool)
        st.session_state["k"] -= 1
        if st.session_state["k"] > 0:
            next = st.button(
                "Next", on_click=solo_quizz, args=(st.session_state["data"],)
            )
        elif st.session_state["k"] == 0:
            display_grade()
            full_reload = st.button("Full reload", on_click=full_reload)
