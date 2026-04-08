import streamlit as st
import xml.etree.ElementTree as ET
import pandas as pd

st.set_page_config(page_title="Leitor de XML", layout="wide")

st.title("📄 Leitor de XML")

st.subheader("Adicione seu arquivo XML para vê-lo em forma de tabela.")

uploaded_file = st.file_uploader("Faça upload do arquivo XML", type=["xml"])

def xml_to_table(file):
    tree = ET.parse(file)
    root = tree.getroot()

    dados = []

    def parse_element(element, parent_name=''):
        registro = {}
        for child in element:
            nome_coluna = f"{parent_name}_{child.tag}" if parent_name else child.tag

            if list(child):
                registro.update(parse_element(child, nome_coluna))
            else:
                registro[nome_coluna] = child.text

        return registro

    for item in root.findall('.//*'):
        if len(list(item)) > 1:
            registro = parse_element(item)
            if registro:
                dados.append(registro)

    return pd.DataFrame(dados)


if uploaded_file:
    try:
        df = xml_to_table(uploaded_file)

        if df.empty:
            st.warning("Não foi possível extrair dados estruturados.")
        else:
            st.success("XML processado com sucesso!")

            st.subheader("📊 Visualização dos dados")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')

            excel_file = "relatorio.xlsx"
            df.to_excel(excel_file, index=False)

            with open(excel_file, "rb") as f:
                st.download_button(
                    label="⬇️ Baixar Excel",
                    data=f,
                    file_name="relatorio.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

    except Exception as e:
        st.error(f"Erro ao processar XML: {e}")
