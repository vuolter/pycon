import React from 'react';
import ReactDOM from 'react-dom';
import { ThemeProvider } from 'styled-components';

import { BrowserRouter as Router, Route } from 'react-router-dom';

import { HomePage } from './pages/home';
import { theme } from './theme';

import { Navbar } from 'components/navbar';

import 'reset-css';
import { DonatePage } from 'pages/donate';

ReactDOM.render(
  <ThemeProvider theme={theme}>
    <Router>
      <>
        <Navbar />

        <Route path="/" exact={true} component={HomePage} />
        <Route path="/donate" exact={true} component={DonatePage} />
      </>
    </Router>
  </ThemeProvider>,
  document.getElementById('root') as HTMLElement,
);
