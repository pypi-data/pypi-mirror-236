import React, { useState, useCallback, useEffect, useMemo } from 'react';
import styled from 'styled-components';
import { Cell } from '@jupyterlab/cells';
import { CogniteClient } from '@cognite/sdk/dist/src';
import { Button, Flex, Icon, InputExp } from '@cognite/cogs.js';
import { CodeGenerateFlow, useCopilotContext } from '@cognite/copilot-core';

export const CodeGeneratorInputPanel = ({
  sdk,
  activeCell,
  onClose
}: {
  sdk: CogniteClient;
  activeCell: Cell;
  onClose: () => void;
}) => {
  const [inputValue, setInputValue] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleChange = useCallback(
    (e: any) => {
      setInputValue(e.target.value);
    },
    [setInputValue]
  );

  const { registerFlow, runFlow } = useCopilotContext();
  const generateFlow = useMemo(
    () => new CodeGenerateFlow({ sdk: sdk as any }),
    []
  );

  useEffect(() => {
    const unregisterGenerate = registerFlow({ flow: generateFlow });
    return unregisterGenerate;
  }, [generateFlow, registerFlow]);

  const handleSubmit = useCallback(
    (e: React.FormEvent) => {
      e.preventDefault();
      setIsGenerating(true);

      runFlow(generateFlow, {
        prompt: inputValue
      }).then((response: any) => {
        (activeCell.model as any).value.text = response.content;
        onClose();
      });
    },
    [runFlow, inputValue]
  );

  return (
    <Container>
      <Flex direction="column">
        <Flex direction="row" justifyContent="space-between">
          <CogniteIcon type="Code" size={36} />
          <div style={{ flexGrow: 1, marginLeft: 8 }}>
            <form onSubmit={handleSubmit}>
              <InputExp
                autoFocus
                clearable
                onChange={handleChange}
                size="large"
                fullWidth
                placeholder="Write a prompt to generate code"
                value={inputValue}
              />
            </form>
          </div>
        </Flex>
        <Flex
          direction="row"
          style={{ marginTop: 16 }}
          justifyContent="space-between"
        >
          <Button
            type="secondary"
            size="large"
            style={{ width: 136 }}
            onClick={onClose}
          >
            Cancel
          </Button>
          <Button
            type="primary"
            size="large"
            style={{
              color: '#fff',
              background: !inputValue || isGenerating ? '#b79df1' : '#6F3BE4',
              width: 136
            }}
            disabled={!inputValue || isGenerating}
            onClick={handleSubmit}
          >
            {isGenerating ? 'Generating ...' : 'Generate'}
          </Button>
        </Flex>
      </Flex>
    </Container>
  );
};

const Container = styled.div`
  && {
    width: 312px;
    background: #fff;
    padding: 16px;
    border-radius: 10px;
    box-shadow:
      0px 1px 16px 4px rgba(79, 82, 104, 0.1),
      0px 1px 8px rgba(79, 82, 104, 0.08),
      0px 1px 2px rgba(79, 82, 104, 0.24);
  }
`;

const CogniteIcon = styled(Icon)`
  color: #6f3be4;
  background: #e9e1fb;
  padding: 8px;
  border-radius: 6px;
`;
