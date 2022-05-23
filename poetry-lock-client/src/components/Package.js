import React from 'react'
import { Link } from 'react-router-dom'

import { styled } from '@mui/material/styles'
import Box from '@mui/material/Box'
import Paper from '@mui/material/Paper'
import Grid from '@mui/material/Grid'

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'left',
  color: theme.palette.text.secondary,
}))

const _ = require('lodash')

const Package =({singlePackage})=> { 

  // deal with possible missing property
  const reverseDep = _.get(singlePackage, 'reverseDep')
  const clickable = _.get(singlePackage, 'clickable')
  const nonClickable = _.get(singlePackage, 'non_clickable')

    
  return(

    <Box sx={{ flexGrow: 1 }}>
      <Grid container spacing={2}>
        <Grid item xs={12} md={8}>
          <Item>
            <h1>{singlePackage.name}</h1>
            <h4>Description: {singlePackage.description}</h4>
          </Item>
        </Grid>
        <Grid item xs={6} md={8}>
          <Item>
            Reverse dependency: {reverseDep && <h4>
              <Link style={{ textDecoration: 'none' }}  to={`/view/${reverseDep}`}>{reverseDep}</Link></h4>}
          </Item>
        </Grid>
        <Grid item xs={6} md={4}>
          <Item>
          Dependencies: {clickable && <h4> 
              {clickable.map((ck, index) => <li key={index}><Link style={{ textDecoration: 'none' }} to={`/view/${ck}`}>{ck}</Link></li>)}</h4>}
            {nonClickable && <h4>{nonClickable.map((ck, index) => <li key={index}>{ck}</li>)}</h4>}
          </Item>
        </Grid>
      </Grid>
    </Box>

  )
}

export default Package