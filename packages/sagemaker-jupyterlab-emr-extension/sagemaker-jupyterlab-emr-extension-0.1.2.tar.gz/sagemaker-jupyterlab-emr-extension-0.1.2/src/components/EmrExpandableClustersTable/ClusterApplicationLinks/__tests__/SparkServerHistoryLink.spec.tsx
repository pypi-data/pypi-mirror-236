import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { SparkServerHistoryLink } from '../SparkServerHistoryLink';
import { i18nStrings } from '../../../../constants/i18n';

const expandClusterStrings = i18nStrings.Clusters.expandCluster;

describe('SparkServerHistoryLink', () => {
  it('renders the component without errors', () => {
    const { getByText } = render(
      <SparkServerHistoryLink accountId="accountId" persistentAppUIId="uiId" setIsError={() => {}} />,
    );

    // You can use RTL queries to assert that specific elements are present based on your component's structure
    expect(getByText(expandClusterStrings.SparkHistoryServer)).toBeInTheDocument();
  });

  it('calls setIsError when clicked while not loading', () => {
    const setIsErrorMock = jest.fn();

    const { getByText } = render(
      <SparkServerHistoryLink accountId="accountId" persistentAppUIId="uiId" setIsError={setIsErrorMock} />,
    );

    const link = getByText(expandClusterStrings.SparkHistoryServer);

    // Simulate a click on the link
    fireEvent.click(link);

    // Assert that setIsErrorMock was called
    expect(setIsErrorMock).toHaveBeenCalledWith(false);
  });

  //TODO: Fix this test once error handling is added
  xit('does not call setIsError when clicked while loading', () => {
    const setIsErrorMock = jest.fn();

    const { getByText } = render(
      <SparkServerHistoryLink accountId="accountId" persistentAppUIId="uiId" setIsError={setIsErrorMock} />,
    );

    const link = getByText('Spark History Server');

    // Simulate a click on the link
    fireEvent.click(link);

    // Assert that setIsErrorMock was not called
    expect(setIsErrorMock).not.toHaveBeenCalled();
  });
});
