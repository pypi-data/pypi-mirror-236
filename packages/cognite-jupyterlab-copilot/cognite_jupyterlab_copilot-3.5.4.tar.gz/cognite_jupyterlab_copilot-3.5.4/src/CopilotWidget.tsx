import React, { useCallback, useMemo, useState } from 'react';
import { CogniteClient } from '@cognite/sdk/dist/src';
import { Menu } from '@cognite/cogs.js';
import { ReactWidget } from '@jupyterlab/apputils';
import { Cell } from '@jupyterlab/cells';
import { Copilot } from '@cognite/copilot-core';
import { CodeGeneratorInputPanel } from './components/CodeGeneratorInputPanel';

/**
 * A Lumino ReactWidget that wraps a CopilotMenu.
 */
export const CopilotWidget: React.FC<any> = ({
  activeCell,
  sdk
}: {
  activeCell: Cell;
  sdk: CogniteClient;
}): any => {
  return ReactWidget.create(
    <div
      id="copilot_widget_root"
      style={{
        position: 'relative',
        zIndex: 100,
        height: '100vh',
        width: '100vw',
        pointerEvents: 'none'
      }}
    >
      <Copilot showChatButton={false} sdk={sdk as any}>
        <CopilotMenu activeCell={activeCell} sdk={sdk} />
      </Copilot>
    </div>
  );
};

const CopilotMenu: React.FC<any> = ({
  activeCell,
  sdk
}: {
  activeCell: Cell;
  sdk: CogniteClient;
}): JSX.Element => {
  const [showRootMenu, setShowRootMenu] = useState(true);
  const [showCodeGenerator, setShowCodeGenerator] = useState(false);

  const onGenerateCodeClick = useCallback(() => {
    setShowRootMenu(false);
    setShowCodeGenerator(true);
  }, [setShowRootMenu, setShowCodeGenerator]);

  // calculate widget position
  const { right, top } = useMemo(() => {
    const rect = activeCell.node.getBoundingClientRect();
    return {
      right: window.innerWidth - rect.width - rect.left + 187,
      top: rect.top
    };
  }, [activeCell]);

  return (
    <div
      id="copilot_menu_root"
      style={{
        height: '100vh',
        width: '100vw',
        pointerEvents: 'none'
      }}
    >
      {showRootMenu && (
        <div
          id="copilot_main_menu"
          style={{
            position: 'absolute',
            right,
            top,
            pointerEvents: 'auto',
            paddingTop: 36
          }}
        >
          <Menu>
            <Menu.Header>Cognite AI</Menu.Header>
            <Menu.Item
              icon="Code"
              iconPlacement="left"
              onClick={onGenerateCodeClick} // TODO: figure out why tf onMouseUp doesn't work
            >
              Generate code
            </Menu.Item>
            <Menu.Item icon="Edit" iconPlacement="left" disabled>
              Edit code
            </Menu.Item>
            <Menu.Item icon="LightBulb" iconPlacement="left" disabled>
              Explain code
            </Menu.Item>
            <Menu.Item icon="Bug" iconPlacement="left" disabled>
              Fix code errors
            </Menu.Item>
          </Menu>
        </div>
      )}
      {showCodeGenerator && (
        <div
          id="copilot_generator_menu"
          style={{
            position: 'absolute',
            right,
            top,
            pointerEvents: 'auto'
          }}
        >
          <CodeGeneratorInputPanel
            sdk={sdk}
            activeCell={activeCell}
            onClose={() => setShowCodeGenerator(false)}
          />
        </div>
      )}
    </div>
  );
};
