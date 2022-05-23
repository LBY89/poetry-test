import Upload from './components/Upload'
import Package from './components/Package'
import RenderView from './components/RenderView'
import axios from 'axios'
import React from 'react'
import {Button, Container} from '@material-ui/core';
import Alert from '@mui/material/Alert';
import { useState } from 'react'
import {
  Routes,
  Route,
  Link,
  useNavigate,
  useMatch
} from "react-router-dom"

const Notification =({ message }) => {
  if (message === null) {
    return null
  }
  return (
    <div className='notice'>
      {(message &&
        <Alert severity="warning">
          {message}
        </Alert>
      )}
    </div>
  )
}
const App =()=> {
  
  const [selectedFile, setSelectedFile] = useState(null)
  const [view, setView] = useState(JSON.parse(window.localStorage.getItem('dataToView')) || null)
  const [noticeMessage, setNoticeMessage] = useState(null)
  
  const navigate = useNavigate()


  const onFileChange = (event) => { 
    event.preventDefault()
    setSelectedFile(event.target.files[0]); 
  }; 
    
  const onFileUpload = () => { 
    console.log('in upload click');
    
    const formData = new FormData(); 
    formData.append( 
      "file", 
      selectedFile
    ); 
    if (!selectedFile) {
      setNoticeMessage("Please Select a Poetry.lock File")
      setTimeout(()=>{
        setNoticeMessage(null)
      }, 3000)
      return
    }
    axios.post('/upload', formData).then(response => {
      console.log('response', response);
      
      setView(response.data)
      window.localStorage.setItem(
        'dataToView', JSON.stringify(response.data)
      )
    })
    navigate('/view')

  }; 
  
  const match = useMatch("/view/:name")

  const singlePackage = match
    ? view.package.find(p => p.name === match.params.name)
    : null

  return ( 
    <Container>
      <Notification message={noticeMessage}/>
      
      <Button  color="primary" variant="outlined" component={Link} to="/">
        Home
      </Button>&nbsp;&nbsp;
      <Button color="primary" variant="outlined"component={Link} to="/view">
        View
      </Button>

      <Routes>
        <Route path="/view/:name" element={<Package setView={setView} singlePackage={singlePackage}/>}/>
        <Route path="/" element={<Upload 
          setNoticeMessage={setNoticeMessage}
          selectedFile={selectedFile}
          onFileUpload={onFileUpload} 
          onFileChange={onFileChange}/>}/>
        <Route path="/view" element={<RenderView view={view} setView={setView}/>}/>
      </Routes>
    </Container>
  ) 
} 
export default App; 