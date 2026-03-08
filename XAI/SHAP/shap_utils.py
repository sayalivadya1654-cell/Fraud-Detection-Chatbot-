# shap_utils.py
import shap
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def shap_global_explain(model, X, feature_names=None, plot=True):
    """
    Compute and visualize SHAP global feature importance for a model.

    Parameters
    ----------
    model : object
        Trained model (scikit-learn, XGBoost, LightGBM, etc.)
    X : array-like or DataFrame
        Input data used for SHAP explanation.
    feature_names : list of str, optional
        Names of features. If None, and X is a DataFrame, uses column names.
    plot : bool, default=True
        Whether to show the summary plot.

    Returns
    -------
    shap_values : shap._explanation.Explanation
        SHAP values object that can be used for further analysis.
    explainer : shap.Explainer
        SHAP explainer object (useful for local explanations).
    """

    # Convert numpy array to DataFrame if feature names provided
    if isinstance(X, np.ndarray) and feature_names is not None:
        X_df = pd.DataFrame(X, columns=feature_names)
    else:
        X_df = X

    # Use SHAP TreeExplainer if model is tree-based, else default
    try:
        if hasattr(model, "predict_proba"):
            explainer = shap.Explainer(model, X_df)
        else:
            explainer = shap.Explainer(model, X_df)
    except Exception as e:
        print(f"⚠ SHAP explainer creation failed: {e}")
        return None, None

    shap_values = explainer(X_df)

    if plot:
        shap.summary_plot(shap_values, X_df, feature_names=feature_names, show=True)

    return shap_values, explainer

def shap_local_explain(explainer, X_input, feature_names=None, plot=True):
    """
    Compute and visualize SHAP local explanations for a single input.

    Parameters
    ----------
    explainer : shap.Explainer
        Precomputed SHAP explainer
    X_input : array-like or DataFrame
        Input for local explanation (usually a single row)
    feature_names : list of str, optional
        Names of features
    plot : bool, default=True
        Whether to plot local SHAP values

    Returns
    -------
    local_shap_values : shap._explanation.Explanation
        SHAP values for the input
    """

    # Convert input to DataFrame if needed
    if isinstance(X_input, np.ndarray) and feature_names is not None:
        X_input_df = pd.DataFrame(X_input, columns=feature_names)
    else:
        X_input_df = X_input

    local_shap_values = explainer(X_input_df)

    if plot:
        shap.waterfall_plot(local_shap_values[0])  # first row

    return local_shap_values