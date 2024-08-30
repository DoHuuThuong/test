import streamlit as st
from code_runner import run_code_in_docker
from test_cases import get_test_cases
from streamlit_monaco import st_monaco

language = st.selectbox("Select Language", ["Java", "C"])
print(language.lower())
content = st_monaco(
    value="  public class Main {public static void main(String[] args) {int a = 5;int b = 10;System.out.println(a + b);}}",
    height="200px",
    language=f'{language.lower()}',
    lineNumbers=True,
    minimap=False,
    theme="vs-dark",
)

if st.button("Run Code"):
    test_cases = get_test_cases(language)
    
    passed_tests = 0
    total_tests = len(test_cases)

    for test_input, expected_output in test_cases:
        full_code = content  # Modify this if test_input should be part of the code
        
        try:
            output = run_code_in_docker(full_code, language)
        except Exception as e:
            st.error(f"Error running code: {str(e)}")
            continue
        
        if output.strip() == expected_output.strip():
            st.success(f"Test Passed: Input: {test_input}")
            passed_tests += 1
        else:
            st.error(f"Test Failed: Input: {test_input}, Expected: {expected_output}, Got: {output}")

    st.write(f"Passed {passed_tests}/{total_tests} test cases.")
