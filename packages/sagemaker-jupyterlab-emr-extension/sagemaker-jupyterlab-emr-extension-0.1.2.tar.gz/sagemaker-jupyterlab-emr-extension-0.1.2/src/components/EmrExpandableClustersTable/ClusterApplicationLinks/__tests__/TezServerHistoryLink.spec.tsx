import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { TezServerHistoryLink } from '../TezServerHistoryLink';

describe('TezServerHistoryLink', () => {
  it('renders the component without errors', () => {
    const { getByText } = render(
      <TezServerHistoryLink accountId="accountId" persistentAppUIId="uiId" setIsError={() => {}} />,
    );

    expect(getByText('Tez UI')).toBeInTheDocument();
  });

  //TODO: Uncomment when we have a error state handled through API integration
  xit('calls setIsError when clicked while not loading', () => {
    const setIsErrorMock = jest.fn();

    const { getByText } = render(
      <TezServerHistoryLink accountId="accountId" persistentAppUIId="uiId" setIsError={setIsErrorMock} />,
    );

    const link = getByText('Tez UI');
    fireEvent.click(link);

    expect(setIsErrorMock).toHaveBeenCalledWith(false);
  });

  it('does not call setIsError when clicked while loading', () => {
    const setIsErrorMock = jest.fn();

    const { getByText } = render(
      <TezServerHistoryLink accountId="accountId" persistentAppUIId="uiId" setIsError={setIsErrorMock} />,
    );

    const link = getByText('Tez UI');
    const component = getByText('Tez UI');
    component.isLoading = true;

    fireEvent.click(link);
    expect(setIsErrorMock).not.toHaveBeenCalled();
  });
});
