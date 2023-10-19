import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';
import { INotebookTracker } from '@jupyterlab/notebook';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { LabIcon } from '@jupyterlab/ui-components';
import { Widget } from '@lumino/widgets';

import { getSdkClient } from './auth';
import { CopilotWidget } from './CopilotWidget';
import ai_icon_svg from '../assets/LogoAi.svg';
import blank_svg from '../assets/blank.svg';

const aiDisabled = new URLSearchParams(window.location.search).has(
  'aiDisabled'
);

export const aiIcon = new LabIcon({
  name: 'cognite_jupyterlab_copilot:cognite_icon',
  svgstr: aiDisabled ? blank_svg : ai_icon_svg
});

export namespace CommandIDs {
  export const openCopilotDropdown = 'jupyterlab:open-copilot-dropdown-menu';
}

/**
 * A plugin that enables Copilot AI commands in from notebook cell toolbars
 */
export const cogniteCopilotPlugin: JupyterFrontEndPlugin<void> = {
  id: 'cognite_jupyterlab_copilot:button_plugin',
  autoStart: true,
  requires: [INotebookTracker, IThemeManager],
  optional: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, nbTracker: INotebookTracker) => {
    if (aiDisabled) {
      return;
    }

    app.commands.addCommand(CommandIDs.openCopilotDropdown, {
      label: 'Copilot',
      execute: async () => {
        // TODO: don't wait for sdk to open the menu?
        const sdk = await getSdkClient();
        sdk.authenticate();

        const widget: any = CopilotWidget({
          activeCell: nbTracker.activeCell,
          sdk
        });
        Widget.attach(widget, document.body);

        // close the menu when clicking outside of it
        const handleBodyClick = (event: MouseEvent) => {
          const targetEle = event.target as HTMLElement;
          const isWidgetClick =
            targetEle.closest('#copilot_main_menu') ||
            targetEle.closest('#copilot_generator_menu');
          if (!isWidgetClick) {
            widget.dispose();
            document.body.removeEventListener('mouseup', handleBodyClick);
          }
        };
        document.body.addEventListener('mouseup', handleBodyClick);
      }
    });

    console.log(
      'JupyterLab extension cognite_jupyterlab_copilot is activated!'
    );
  }
};

export default cogniteCopilotPlugin;
