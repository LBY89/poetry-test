import React from 'react'
import {
    Link,
  } from "react-router-dom"

import {TableContainer, Table, TableBody, TableRow, TableCell, Paper} from '@material-ui/core';

const RenderView =({view, setView})=> {
    console.log('renderview compo');
    
    // useEffect(()=>{
    //     const viewData = JSON.parse(window.localStorage.getItem('dataToView'))
        
    //     if (viewData) {
    //         setView(viewData)
    //     } 
    // },[setView])
    

    if (view == null) {
        return(
            <div>
                no data
            </div>
        )
    } else {
    
    return(
        <div>

        <h2>There are {view.package.length} packages in your file</h2>
        <TableContainer component={Paper}>
            <Table>
                <TableBody>
                    {view.package.map((pkg,index) => 
                        <TableRow key={index}>
                            <TableCell>
                            <Link style={{ textDecoration: 'none' }} to={`/view/${pkg.name}`}><h4>{pkg.name}</h4></Link>
                            </TableCell>
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </TableContainer>

        </div>
    )
    }

}

export default RenderView