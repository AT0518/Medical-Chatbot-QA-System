from src_code.ocr import read_data, do_ocr
from src_code.mongo_helper import _write_to_db, _read_from_db
from src_code.embedding_helper import embed_helper
from src_code.pinecone_helper import write_to_pinecone, retrival_from_pinecone
from src_code.utils import query_builder
from src_code.call_llm import ask_gemini


def main(create_embedding = False, user_query = None):
    if create_embedding:    
        dataframe = read_data()
        
        ocr_data = do_ocr(dataframe)
        
        write_response = _write_to_db(ocr_data)
        
        if write_response is None:
            return "DB write failed"
        
        
        records = _read_from_db()
        
        embeddings = embed_helper(records)
        
        pinecone_write_result = write_to_pinecone(embeddings)
        
        if pinecone_write_result is None:
                return "pinecone write failed"
    else:
        if user_query is None:
            return "Please Enter User Query"
        
        retrival_result = retrival_from_pinecone(user_query)
        final_prompt = query_builder(user_query, retrival_result)
        final_result = ask_gemini(final_prompt)
        
        if final_result: 
            return final_result
        else:
            return "llm call failed"    
    
 
if __name__ == "__main__":
    user_input = int(input("If you  want to generate embeddings please enter 1 and if you want to call llm please enter 2: "))
    if user_input == 1:
        response = main(create_embedding=True)
        print(response)
        
    
    elif user_input == 2:
        user_question = input("Please Enter your search")
        response = main(user_query = user_question)
        print(response)
    else:
        print("You have entered wrong choice")           
    
    
    

