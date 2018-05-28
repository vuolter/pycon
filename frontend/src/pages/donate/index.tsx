import * as React from 'react';
import { Main } from 'components/main';
import { Title, Paragraph } from 'components/typography';

import { DonationForm } from './donation-form';

export const DonatePage = () => (
  <>
    <Main navbar={true}>
      <Title>Donate!</Title>

      <Paragraph>This page will allow user to donate.</Paragraph>

      <DonationForm />
    </Main>
  </>
);
