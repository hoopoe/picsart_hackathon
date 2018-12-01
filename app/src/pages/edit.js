import React from 'react'
import { Link } from 'gatsby'

import Layout from '../components/layout'
import ImageBox from '../components/image-box'

import Styles from './edit.module.css'

const Filter = props => (
  <div className={Styles.filter}>
    <img src={props.avatar} className={Styles.avatar} alt="" />
    <div className={Styles.description}>
      <h3 className={Styles.filtername}>{props.filtername}</h3>
      <p className={Styles.excerpt}>{props.excerpt}</p>
    </div>
  </div>
)

const EditPage = () => (
  <Layout>
    <div className={Styles.row}>
      <Link to="/">Go back to the homepage</Link>
    </div>

    <div className={Styles.row}>
      <div className={Styles.doubleColumn}>
        <ImageBox />
      </div>
      <div className={Styles.column}>
        <Filter
          filtername="Blur background"
          avatar={require('../images/blur-effect.jpg')}
          excerpt="I'm Jane Doe. Lorem ipsum dolor sit amet, consectetur adipisicing elit."
        />
      </div>
    </div>
  </Layout>
)

export default EditPage
