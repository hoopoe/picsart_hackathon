import React from 'react'
import { Link } from 'gatsby'

import Layout from '../components/layout'

const IndexPage = () => (
  <Layout>
    <p>Welcome to face-tuning App.</p>
    <Link to="/edit/">Let's edit some photos</Link>
  </Layout>
)

export default IndexPage
