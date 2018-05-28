import React from 'react';

import styled from '../../styled';
import { Paragraph } from '../../components/typography';
import { Grid, Column } from '../../components/grid';
import { Button } from '../../components/button';
import { Input } from '../../components/input';

const Form = styled.form`
  .mdc-text-field {
    width: 100%;
  }
`;

export class DonationForm extends React.Component<{}> {
  state = {
    fullName: '',
    amount: '',
  };

  render() {
    return (
      <Form>
        <Paragraph>
          Hi, thanks for considering to donate to Python Italia.
        </Paragraph>
        <Grid>
          <Column cols={4}>
            <Input
              label="Full Name"
              onChange={e => this.setState({ fullName: e.target.value })}
              value={this.state.fullName}
              helpText={`If you want your name to be shown fill this field,
                you can also omit it and make an anonymous donation`}
            />
          </Column>

          <Column cols={4}>
            <Input
              label="Donation amount (EUR)"
              onChange={e => this.setState({ amount: e.target.value })}
              value={this.state.amount}
              type="number"
              helpText="Help text"
            />
          </Column>
        </Grid>

        <Button>Send donation</Button>
      </Form>
    );
  }
}
