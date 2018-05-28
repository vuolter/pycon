import React from 'react';
import TextField, {
  Input as MaterialInput,
  HelperText,
} from '../../vendor/react-material/text-field';

type Props = {
  label?: string;
  type?: string;
  helpText?: string;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
};

export const Input: React.SFC<Props> = ({
  label,
  helpText,
  type,
  value,
  onChange,
}) => (
  <TextField
    label={label}
    box={true}
    type={type || 'text'}
    showHelperTextToScreenReader={true}
    helperText={helpText && <HelperText>{helpText}</HelperText>}
  >
    <MaterialInput onChange={onChange} value={value} />
  </TextField>
);
