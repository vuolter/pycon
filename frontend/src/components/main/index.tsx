import React from 'react';
import styled from '../../styled';

type Props = {
  // TODO: find a better name to describe when
  // there is a margin top to take the navbar into
  // account
  navbar?: boolean;
};

const BaseMain: React.SFC<Props> = ({ navbar, children, ...props }) => (
  <main {...props}>{children}</main>
);

export const Main = styled(BaseMain)`
  width: 90%;
  max-width: 900px;
  margin: 0 auto;

  position: relative;
  overflow: hidden;

  margin-top: ${props => (props.navbar ? 70 : 0)}px;
`;
