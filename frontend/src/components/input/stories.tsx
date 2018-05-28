import React from 'react';
import { storiesOf } from '@storybook/react';

import { Input } from '.';
import { Title } from '../typography';

storiesOf('Input', module).add('simple', () => (
  <div>
    <Title level={6}>Simple input example</Title>
    <Input label="example" />
  </div>
));
