import openai
import streamlit as st


# App title
st.set_page_config(page_title="🤖💬 OpenAI Chatbot")
openai_api_key = st.secrets['OPENAI_API_KEY']

added_information = """Microsoft Corporation adalah sebuah perusahaan teknologi multinasional Amerika yang bermarkas di Redmond, Washington. 
Perusahaan ini didirikan oleh Bill Gates dan Paul Allen pada tanggal 4 April 1975. 
Produk perangkat lunak terkenal dari Microsoft antara lain adalah sistem operasi Windows, aplikasi produktivitas Microsoft 365, dan browser web Edge. 
Produk perangkat keras unggulan mereka adalah konsol video game Xbox dan lineup komputer pribadi layar sentuh Microsoft Surface. 
Pada tahun 2022, Microsoft menempati peringkat No. 14 dalam daftar Fortune 500 perusahaan terbesar Amerika Serikat berdasarkan total pendapatan; 
perusahaan ini merupakan pembuat perangkat lunak terbesar di dunia berdasarkan pendapatan pada tahun 2022."""

def get_response(user_prompts):

    system_prompt = "Anda adalah AI asisten untuk sebuah perusahaan bernama Microsoft Corporation. Anda harus berbicara dalam bahasa Indonesia formal dan tidak boleh merespons menggunakan bahasa inggris."
    messages = [
        {"role": "system", "content": f"{system_prompt} berikut merupakan informasi tambahan mengenai perusahaan {added_information}. Anda hanya menjawab pertanyaan beradasrkan informasi yang telah diberikan dan secara sopan menolak untuk menjawab pertanyaan yang tidak ada di dalam informasi yang telah diberikan"},
        # {"role":"user", "content": """hapalkan text di bawah, dan jawab setiap pertanyaan merujuk pada apa yang kamu hapalkan! Kapan Wide Technology Indonesia didirikan? Wide Technology Indonesia di dirikan tahun 2000 sebagai PT Aprisma Indonesia Siapa CEO Wide Technology Indonesia? Pardjo Yap Produk apa saja yang ada di PT. Wide Technology Indonesia? Primecash, PrismaGateway, PrimeCash COB, PrimeCash Fast, Digital Business Platform, WideKYC Apa produk atau layanan utama yang ditawarkan perusahaan ini? System Integration, System Performance Review Apa visi dan misi perusahaan? We work with banks and financial institutes, each with their own tier and business needs, to create excellent solutions in order to satisfy their corporate, SME, and retail needs."""}
        # {"role": "user", "content": "Kapan Wide Technology Indonesia didirikan?"},
        # {"role": "assistant", "content": "Wide Technology Indonesia di dirikan tahun 2000 sebagai PT Aprisma Indonesia"},
        # {"role": "user", "content": "Siapa CEO Wide Technology Indonesia?"},
        # {"role": "assistant", "content":"Pardjo Yap"},
        # {"role": "user", "content":"Produk apa saja yang ada di PT. Wide Technology Indonesia?"},
        # {"role":"assistant", "content":"Primecash, PrismaGateway, PrimeCash COB, PrimeCash Fast, Digital Business Platform, WideKYC"},
        # {"role": "user", "content": "Apa produk atau layanan utama yang ditawarkan perusahaan ini?"},
        # {"role":"assistant", "content":"System Integration, System Performance Review"},
        # {"role": "user", "content":"Apa visi dan misi perusahaan?"},
        # {"role":"assistant", "content":"We work with banks and financial institutes, each with their own tier and business needs, to create excellent solutions in order to satisfy their corporate, SME, and retail needs."}
        ]
    
    
    for user_prompt in user_prompts:
        # print(user_prompt)
        messages.append(user_prompt)

    # messages[-1]['content'] += 'Do not give me any information about procedures and service features that are not mentioned in the PROVIDED CONTEXT.'



    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # model="gpt-4",
        messages=messages,
        temperature=0.3,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
    )
    
    return completion.choices[0].message

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Halo, ada yang bisa dibantu?"}]

def main():

    with st.sidebar:
        st.title('🤖💬 OpenAI Chatbot')
        # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Halo, ada yang bisa dibantu?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():

        openai.api_key = openai_api_key

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.spinner('Thinking...'):
            msg = get_response(st.session_state.messages)

        
        st.session_state.messages.append(msg)
        st.chat_message("assistant").write(msg.content)

if __name__ == '__main__':
    main()