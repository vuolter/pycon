import React from 'react';

import styled from '../../styled';
import { Paragraph } from '../../components/typography';
import { Grid, Column } from '../../components/grid';
import TextField, {
  Input,
  HelperText,
} from '../../vendor/react-material/text-field';
import { Button } from '../../components/button';

const Form = styled.form`
  .mdc-text-field {
    width: 100%;
  }
`;

export class DonationForm extends React.Component<{}> {
  render() {
    return (
      <Form>
        <Paragraph>
          Hi, thanks for considering to donate to Python Italia.
        </Paragraph>
        <Grid>
          <Column cols={4}>
            <TextField
              label="Full Name"
              box={true}
              showHelperTextToScreenReader={true}
              helperText={
                <HelperText>
                  If you want your name to be shown fill this field, you can
                  also omit it and make an anonymous donation
                </HelperText>
              }
            >
              <Input />
            </TextField>
          </Column>

          <Column cols={4}>
            <TextField
              label="Donation amount (EUR)"
              box={true}
              type="number"
              showHelperTextToScreenReader={true}
              helperText={<HelperText>Help text</HelperText>}
            >
              <Input />
            </TextField>
          </Column>
        </Grid>

        <Button>Send donation</Button>
      </Form>
    );
  }
}
