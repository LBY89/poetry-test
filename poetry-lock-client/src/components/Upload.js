import React from 'react'
//import FileUploadIcon from '@mui/icons-material/FileUpload'
import {Button} from '@material-ui/core';

const Upload =({onFileUpload, onFileChange, selectedFile, setNoticeMessage})=> {
    const fileData = () => { 
    
        if (selectedFile) { 
          return ( 
            <div> 
              <h4>{selectedFile.name}</h4>
            </div> 
          ); 
        } else { 
          return ( 
            <div> 
              <br /> 
              <h4>Click 'Choose file' to choose</h4> 
            </div> 
          ); 
        } 
      }; 
    return(
        <div> 
             <br/>
             <label  htmlFor="filePicker" style={{ background:"green", padding:"5px 10px" }}>
              Choose file
              </label>
              <input id="filePicker" style={{visibility:"hidden"}} type={"file"} accept={".lock, .py, .png"} onChange={onFileChange}/>
            {/* <input type="file" accept=".lock, .py"  onChange={onFileChange} />  */}
            <Button color="secondary" variant="outlined" onClick={onFileUpload}> 
                Upload! 
            </Button> 
            {fileData()} 

        </div> 
    )
}

export default Upload