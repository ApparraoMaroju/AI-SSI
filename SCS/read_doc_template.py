import win32com.client
import os

def read_doc_file(file_path):
    """Read content from a .doc file using COM interface"""
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    
    try:
        doc = word.Documents.Open(file_path)
        
        # Get full text
        full_text = doc.Content.Text
        
        # Get headings and structure
        print("=" * 80)
        print("DOCUMENT STRUCTURE AND CONTENT")
        print("=" * 80)
        
        # Print the full content
        print(full_text)
        
        doc.Close()
    finally:
        word.Quit()

if __name__ == "__main__":
    file_path = r"c:\Apparao Maroju\AI-SSI\Templates\Temp-Input\SLS_Test_Strategy_F_v0.1.doc"
    read_doc_file(file_path)
