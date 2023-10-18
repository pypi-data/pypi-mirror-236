import React from 'react';
import { cx } from '@emotion/css';
import { i18nStrings } from '../../../constants/i18n';
import { EmrClusterPluginClassNames } from '../../../constants/common';
import * as styles from './styles';

interface Props {
  accountId: string;
  persistentAppUIId: string;
  setIsError: (isError: boolean) => void;
}

const expandClusterStrings = i18nStrings.Clusters.expandCluster;
const expandClusterHistoryClassNames = EmrClusterPluginClassNames.HistoryLink;

const SparkServerHistoryLink: React.FunctionComponent<Props> = ({ persistentAppUIId, accountId, setIsError }) => {
  const [isLoading] = React.useState(false);

  const handleSparkServerHistoryClick = () => {
    if (isLoading) {
      return;
    }

    // TODO: call API handler to create spark server history url
    setIsError(false);
  };

  //TODO: Replace loading with Spinner icon
  return (
    <div className={styles.linkContainer} onClick={handleSparkServerHistoryClick}>
      <div className={cx(expandClusterHistoryClassNames, styles.link)}>{expandClusterStrings.SparkHistoryServer}</div>
      {isLoading && 'Loading...'}
    </div>
  );
};

export { SparkServerHistoryLink };
