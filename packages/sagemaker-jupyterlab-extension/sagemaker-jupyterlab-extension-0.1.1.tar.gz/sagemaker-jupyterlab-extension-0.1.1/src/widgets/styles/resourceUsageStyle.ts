import { css } from '@emotion/css';

/** JupyterLabs uses an 4px grid */
const Padding = {
  small: '4px',
  medium: '8px',
  mediumLarge: '12px',
  sixteen: '16px',
  large: '20px',
  xl: '24px',
  xxl: '28px',
  xxxl: '32px',
};

const FontFamily =
  "-apple - system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans - serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol'";
const FontColor = 'rgba(0, 0, 0, 0.87)';

const KernelMetricContainer = css`
  border-bottom: solid 1px var(--sm-border-color2);
`;
const LayoutColor = '#eeeeee';
const LayoutColor3 = '#bdbdbd';
const BorderColor2 = '#e0e0e0';
const FontSize = '13px';

const MetricsWindowStyle = css`
  background-color: ${LayoutColor};
  border: solid 1px ${BorderColor2};
  color: ${FontColor};
  font-size: ${FontSize};
  position: fixed;
  bottom: 25px;
`;

const MetricsContainerStyle = css`
  margin: 0 ${Padding.mediumLarge} ${Padding.medium};
`;

const MetricsTitleStyle = css`
  font-weight: bold;
  margin: ${Padding.medium} 0 0 ${Padding.medium};
`;

const MetricsDescriptionStyle = css`
  margin: 0 ${Padding.mediumLarge} 0 ${Padding.sixteen};
`;

const SingleProgressBarStyle = css`
  border-radius: 10px;
  height: 100%;
  width: 30px;
`;

const RemoteStatusContainer = css`
  height: 24px;
  max-height: 24px;
  font-size: 13px;
  font-family: ${FontFamily};
  color: ${FontColor};
  line-height: 24px;
  padding: 0 5px;

  &:hover {
    background-color: ${LayoutColor3};
  }
`;

const SpacerStyle = css`
  padding-left: 4px;
`;

const SingleMetricContainer = css`
  display: flex;
  justify-content: flex-start;
  align-items: center;
  margin: 6px 12px;
`;

const SingleMetricLabel = css`
  color: ${FontColor};
  font-size: ${FontSize};
  padding-right: 5px;
`;

const StatusBarProgressBarContainerStyle = css`
  border-radius: 10px;
  width: 40px;
  margin: 0 0 2px 4px;
  height: 6px !important;
`;

const SingleProgressBarContainerStyle = css`
  border-radius: 10px;
  display: inline-block;
  width: 40px;
  height: 8px;
`;

const ResourceWidgetConatiner = css`
  display: flex;
  align-items: center;
`;

export {
  KernelMetricContainer,
  MetricsContainerStyle,
  MetricsTitleStyle,
  MetricsDescriptionStyle,
  MetricsWindowStyle,
  SingleProgressBarStyle,
  RemoteStatusContainer,
  SpacerStyle,
  StatusBarProgressBarContainerStyle,
  SingleMetricContainer,
  SingleMetricLabel,
  SingleProgressBarContainerStyle,
  ResourceWidgetConatiner,
};
