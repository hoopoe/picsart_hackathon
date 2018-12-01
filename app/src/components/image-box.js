import React from 'react'
import { Link } from 'gatsby'
import Styles from './image-box.module.css'

const ImageBox = () => (
  <section className={Styles.container}>
    <section className={Styles.dropbox}>
      <h4>Drop a photo here to upload</h4>
    </section>
  </section>
)

export default ImageBox
