import streamlit as st
import replicate

# App title
st.set_page_config(page_title="🦙💬 Llama Chatbot")
replicate_api = st.secrets['REPLICATE_API_TOKEN']


microsoft_information = """
<<SYS>> Berikut merupakan informasi tambahan yang perlu kamu ingat, Microsoft Corporation adalah sebuah perusahaan teknologi multinasional Amerika yang bermarkas di Redmond, Washington. 
Perusahaan ini didirikan oleh Bill Gates dan Paul Allen pada tanggal 4 April 1975. 
Produk perangkat lunak terkenal dari Microsoft antara lain adalah sistem operasi Windows, aplikasi produktivitas Microsoft 365, dan browser web Edge. 
Produk perangkat keras unggulan mereka adalah konsol video game Xbox dan lineup komputer pribadi layar sentuh Microsoft Surface. 
Pada tahun 2022, Microsoft menempati peringkat No. 14 dalam daftar Fortune 500 perusahaan terbesar Amerika Serikat berdasarkan total pendapatan; 
perusahaan ini merupakan pembuat perangkat lunak terbesar di dunia berdasarkan pendapatan pada tahun 2022. <<SYS>>
"""

def get_response(prompt_input):
    string_dialogue = f" {microsoft_information}"
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "[INST] " + dict_message["content"] +" [/INST]" + "\n"
        else:
            string_dialogue +=  dict_message["content"] + "\n"
    
    input_message = f"{string_dialogue} {prompt_input}"

    output = replicate.run(
                            'replicate/llama70b-v2-chat:2d19859030ff705a87c746f7e96eea03aefb71f166725aee39692f1476566d48',
                            input={
                                "system_prompt": "Anda adalah AI asisstant untuk sebuah perusahaan bernama Microsoft Corporation. Anda harus berbicara dalam bahasa Indonesia yang formal. Anda hanya menjawab pertanyaan beradasarkan informasi yang diberikan dan secara sopan menolak untuk menjawab pertanyaan yang tidak ada di dalam informasi yang telah diberikan",
                                "prompt": input_message,
                                "temperature":0.01, 
                                "top_p":1, 
                                "max_length":256, 
                                "repetition_penalty":1
                                }
                            )
    return output

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Halo, ada yang bisa dibantu?"}]

def main():
    with st.sidebar:
        st.title('🦙 Llama 2 Chatbot')
        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)
        # pass

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "Halo, ada yang bisa dibantu?"}]

    # Display or clear chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input(disabled=not replicate_api):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = get_response(prompt)
                placeholder = st.empty()
                full_response = ''
                for item in response:
                    full_response += item
                    placeholder.markdown(full_response)

                placeholder.markdown(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)

if __name__ == '__main__':
    main()