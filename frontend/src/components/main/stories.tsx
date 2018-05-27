import React from 'react';
import { storiesOf } from '@storybook/react';

import { Main } from '.';

storiesOf('Main', module)
  .add('default', () => <Main>Hello world</Main>)
  .add('with nav bar margin', () => <Main navbar={true}>Hello world</Main>);
