import { CogniteClient } from '@cognite/sdk';

export const getSdkClient = () =>
  new Promise<CogniteClient>(resolve => {
    // handle 'getToken' response from parent window
    window.addEventListener(
      'message',
      (event: MessageEvent) => {
        if (
          typeof event.data === 'object' &&
          'token' in event.data &&
          'baseUrl' in event.data &&
          'project' in event.data
        ) {
          const { token, baseUrl, project } = event.data;
          resolve(
            new CogniteClient({
              appId: 'LLM-hub-server',
              project,
              baseUrl,
              getToken: async () => token
            })
          );
        }
      },
      { capture: false, once: true }
    );
    window?.top?.postMessage('getToken', '*');
  });
