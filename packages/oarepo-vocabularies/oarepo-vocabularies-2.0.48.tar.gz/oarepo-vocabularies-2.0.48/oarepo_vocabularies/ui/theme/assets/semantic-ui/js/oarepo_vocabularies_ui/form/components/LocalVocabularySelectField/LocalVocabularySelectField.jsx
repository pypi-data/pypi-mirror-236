import React from "react";
import { SelectField } from "react-invenio-forms";
import { useFormConfig } from "@js/oarepo_ui";
import {
  serializeVocabularyItem,
} from "@js/oarepo_vocabularies";
import { useFormikContext, getIn } from "formik";
import PropTypes from "prop-types";

// the idea is for this component to be a simple searchable single or multiple selection drop down
// that would handle things items that are going to be placed inside the formConfig (HTML). From what I see, all the vocabularies
// we have except institutions vocabulary which is a bit bigger could be easily handled by this component meaning:
// access-rights, contributor-roles, countries, funders, item-relation-types, languages, licences (rights), resource-types, subject-categories
// need form config to contain vocabularis.[languages, licenses, resourceTypes]

export const deserializeLocalVocabularyItem = (item) => {
  return Array.isArray(item)
    ? item.map((item) => deserializeLocalVocabularyItem(item))
    : item.id;
};


export const LocalVocabularySelectField = ({
  fieldPath,
  multiple,
  optionsListName,
  helpText,
  ...uiProps
}) => {
  const {
    formConfig: { vocabularies },
  } = useFormConfig();
  let optionsList = [];
  if (vocabularies[optionsListName]?.all !== undefined) {
    optionsList = vocabularies[optionsListName].all;
  } else {
    console.error(
      `Do not have options for ${optionsListName} inside:`,
      vocabularies
    );
  }

  const { values, setFieldTouched } = useFormikContext();
  const value = deserializeLocalVocabularyItem(
    getIn(values, fieldPath, multiple ? [] : {})
  );
  return (
    <React.Fragment>
      <SelectField
        // formik exhibits strange behavior when you enable search prop to semantic ui's dropdown i.e. handleBlur stops working - did not investigate the details very deep
        // but imperatively calling setFieldTouched gets the job done
        onBlur={() => setFieldTouched(fieldPath)}
        search
        fieldPath={fieldPath}
        multiple={multiple}
        options={optionsList}
        onChange={({ e, data, formikProps }) => {
          formikProps.form.setFieldValue(
            fieldPath,
            serializeVocabularyItem(data.value)
          );
        }}
        value={value}
        {...uiProps}
      />
      <label style={{ fontWeight: "bold" }}>{helpText}</label>
    </React.Fragment>
  );
};

LocalVocabularySelectField.propTypes = {
  fieldPath: PropTypes.string.isRequired,
  multiple: PropTypes.bool,
  optionsListName: PropTypes.string.isRequired,
  helpText: PropTypes.string,
};
