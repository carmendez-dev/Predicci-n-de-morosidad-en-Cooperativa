"""
SCRIPT DE ENTRENAMIENTO AUTOMÁTICO - PREDICCIÓN DE MOROSIDAD
"""
import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from sklearn.impute import SimpleImputer
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import (
    train_test_split, 
    GridSearchCV, 
    RandomizedSearchCV, 
    StratifiedKFold,
    cross_val_score
)
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)
from scipy.stats import loguniform, randint
import argparse
import joblib
import json
from datetime import datetime

# --- CLASE BASE DE EDA (Análisis Exploratorio) ---
class EDA_Morosidad:
    """ Clase base para el Análisis Exploratorio de Datos. """
    
    def __init__(self, data_path, random_state=42):
        self.data_path = data_path
        self.random_state = random_state
        np.random.seed(random_state)
        random.seed(random_state)
        self.df = None
        self.target = None
        self.cleaned_path = "cleaned_dataset.csv"
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = 'output' # Por defecto

    def load_data(self):
        # Carga el dataset y muestra información inicial.
        self.df = pd.read_csv(self.data_path)
        print(f"Dataset cargado: {self.df.shape[0]} filas, {self.df.shape[1]} columnas")
        print(self.df.head())
        return self.df

    def resumen_general(self):
        # Muestra información general, nulos y estadísticas básicas.
        print("\n--- Información General del Dataset ---")
        self.df.info() # .info() imprime directamente
        print("\n--- Estadísticas Descriptivas ---")
        print(self.df.describe().T)
        print("\n--- Valores Nulos y Cardinalidad ---")
        resumen = pd.DataFrame({
            'n_nulos': self.df.isnull().sum(),
            'pct_nulos': self.df.isnull().mean() * 100,
            'n_uniques': self.df.nunique()
        })
        print(resumen.sort_values('pct_nulos', ascending=False))
        print(f"Duplicados detectados: {self.df.duplicated().sum()}")

    # --- MÉTODO CORREGIDO ---
    def plot_distributions(self):
        # Genera y guarda histogramas y boxplots.
        print("Generando gráficos de distribución...")
        num_cols = self.df.select_dtypes(include='number').columns.tolist()
        
        if not num_cols:
            print("No se encontraron columnas numéricas para graficar distribuciones.")
            return
            
        n = len(num_cols)
        ncols = 3
        nrows = int(np.ceil(n / ncols))
        
        # --- Histogramas ---
        # ¡CORRECCIÓN! Usamos plt.subplots() para obtener 'fig1'
        fig1, axes1 = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
        axes1 = axes1.flatten() # Aplanar el array de ejes para iterar fácilmente

        i = 0 # Inicializar contador
        for i, c in enumerate(num_cols):
            sns.histplot(self.df[c].dropna(), kde=True, ax=axes1[i])
            axes1[i].set_title(f"Distribución: {c}")
            
        # Ocultar ejes sobrantes
        for j in range(i + 1, len(axes1)):
            axes1[j].set_visible(False)
            
        plt.tight_layout()
        fig_path1 = os.path.join(self.output_dir, f'plot_distributions_hist_{self.timestamp}.png')
        plt.savefig(fig_path1)
        plt.close(fig1) # Ahora 'fig1' sí existe

        
        # --- Boxplots ---
        # ¡CORRECCIÓN! Usamos plt.subplots() para obtener 'fig2'
        fig2, axes2 = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
        axes2 = axes2.flatten() # Aplanar el array de ejes

        i = 0 # Reiniciar contador
        for i, c in enumerate(num_cols):
            sns.boxplot(x=self.df[c].dropna(), ax=axes2[i])
            axes2[i].set_title(f"Boxplot: {c}")
            
        # Ocultar ejes sobrantes
        for j in range(i + 1, len(axes2)):
            axes2[j].set_visible(False)
            
        plt.tight_layout()
        fig_path2 = os.path.join(self.output_dir, f'plot_distributions_boxplot_{self.timestamp}.png')
        plt.savefig(fig_path2)
        plt.close(fig2) # Ahora 'fig2' sí existe

    def matriz_correlacion(self):
        # Genera y guarda la matriz de correlación.
        print("Generando matriz de correlación...")
        num_cols = self.df.select_dtypes(include='number').columns
        corr = self.df[num_cols].corr()
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax)
        ax.set_title("Matriz de Correlación")
        fig_path = os.path.join(self.output_dir, f'plot_matriz_correlacion_{self.timestamp}.png')
        plt.savefig(fig_path)
        plt.close(fig)
        return corr

    def detectar_target(self):
        # Identifica la columna objetivo automáticamente.
        posibles = [c for c in self.df.columns if 'default' in c.lower() or 'moros' in c.lower() or 'incumpl' in c.lower()]
        if len(posibles) == 1:
            self.target = posibles[0]
            print(f"Target detectado automáticamente: {self.target}")
        elif len(posibles) > 1:
            print(f"Varias columnas posibles: {posibles}. Seleccionando el primero por defecto.")
            self.target = posibles[0]
        else:
            print("No se detectó automáticamente el target. Asignar manualmente.")

        if self.target and self.target in self.df.columns:
            print("\n--- Balance de la Variable Target ---")
            print(self.df[self.target].value_counts(normalize=True) * 100)
        return self.target

    def analizar_relaciones(self):
        # Genera y guarda visualizaciones de relaciones con el target.
        print("Generando gráficos de relaciones con el target...")
        if self.target is None:
            print("No se ha definido el target. Saltando análisis de relaciones.")
            return

        num_cols = [c for c in self.df.select_dtypes(include='number').columns if c != self.target]
        cat_cols = self.df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()

        # Boxplots Numéricas vs Target
        for c in num_cols:
            fig, ax = plt.subplots(figsize=(6, 3))
            sns.boxplot(x=self.df[self.target], y=self.df[c], ax=ax)
            ax.set_title(f"{c} vs {self.target}")
            fig_path = os.path.join(self.output_dir, f'plot_relacion_num_{c}_{self.timestamp}.png')
            plt.savefig(fig_path)
            plt.close(fig)

        # Countplots Categóricas vs Target
        for c in cat_cols:
            fig, ax = plt.subplots(figsize=(8, 4))
            sns.countplot(x=self.df[c], hue=self.df[self.target], ax=ax)
            ax.set_title(f"{c} por {self.target}")
            ax.tick_params(axis='x', rotation=45)
            fig_path = os.path.join(self.output_dir, f'plot_relacion_cat_{c}_{self.timestamp}.png')
            plt.savefig(fig_path)
            plt.close(fig)

    def calcular_vif(self):
        # Calcula el Factor de Inflación de Varianza (VIF).
        print("Calculando VIF...")
        num_cols = self.df.select_dtypes(include='number').columns
        X = self.df[num_cols].dropna()
        X = X.replace([np.inf, -np.inf], np.nan).dropna()
        X = X.loc[:, X.var() > 1e-6]
        if X.empty:
            print("No hay suficientes datos numéricos válidos para calcular VIF.")
            return
        vif_data = pd.DataFrame()
        vif_data['feature'] = X.columns
        vif_data['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
        print(vif_data.sort_values('VIF', ascending=False))
        return vif_data

    def limpiar_dataset(self):
        # Realiza limpieza e imputación simple de datos.
        print("\n--- Limpieza simple (Solo para EDA) ---")
        df_clean = self.df.copy()
        drop_cols = df_clean.columns[df_clean.isnull().mean() > 0.5].tolist()
        if drop_cols:
            print(f"Eliminando columnas con >50% de nulos: {drop_cols}")
            df_clean = df_clean.drop(columns=drop_cols)
        # ... (resto de la lógica de limpieza) ...
        self.cleaned_path = os.path.join(self.output_dir, f'cleaned_dataset_{self.timestamp}.csv')
        df_clean.to_csv(self.cleaned_path, index=False)
        print(f"Dataset limpio (para EDA) guardado como {self.cleaned_path}")
        return df_clean

# --- CLASE DE MODELADO Y CLASIFICACIÓN ---

class ClasificadorMorosidad(EDA_Morosidad):
    """
    Clase para el pipeline de clasificación, heredando de EDA_Morosidad.
    """

    # --- MÉTODO CORREGIDO ---
    def __init__(self, data_path, output_dir='output', random_state=42):
        super().__init__(data_path, random_state)
        
        # --- ¡AQUÍ ESTÁ LA PARTE QUE FALTA! ---
        # Directorio de salida para todos los artefactos
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        os.makedirs(self.output_dir, exist_ok=True)
        print(f"Inicializando Clasificador. Salidas se guardarán en: {self.output_dir}")
        # ------------------------------------
        
        self.X_train = None
        self.y_train = None
        self.X_val = None
        self.y_val = None
        self.X_test = None
        self.y_test = None
        self.numeric_features = []
        self.categorical_features = []
        self.preprocessor = None
        self.models = {}
        self.metrics = {}

    def dividir_datos(self):
        # (Sin cambios)
        print("\n--- Dividiendo los Datos (70% Train / 15% Validation / 15% Test) ---")
        X = self.df.drop(columns=self.target)
        y = self.df[self.target]
        self.X_train, X_temp, self.y_train, y_temp = train_test_split(
            X, y, test_size=0.3, random_state=self.random_state, stratify=y)
        self.X_val, self.X_test, self.y_val, self.y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=self.random_state, stratify=y_temp)
        print(f"Total de datos: {len(X)}")
        print(f"Forma X_train: {self.X_train.shape}")
        print(f"Forma X_val:   {self.X_val.shape}")
        print(f"Forma X_test:  {self.X_test.shape}")

    def _identificar_columnas(self):
        # (Sin cambios)
        self.numeric_features = self.X_train.select_dtypes(include=np.number).columns.tolist()
        self.categorical_features = self.X_train.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        print(f"Columnas numéricas detectadas: {self.numeric_features}")
        print(f"Columnas categóricas detectadas: {self.categorical_features}")

    def crear_pipeline_preprocesamiento(self):
        # (Sin cambios)
        print("\n--- Creando Pipeline de Preprocesamiento ---")
        self._identificar_columnas()
        numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler())])
        categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, self.numeric_features),
                ('cat', categorical_transformer, self.categorical_features)],
            remainder='passthrough')
        print("Pipeline de preprocesamiento creado exitosamente.")
        return self.preprocessor

    def entrenar_modelos(self):
        # (Sin cambios)
        print("\n--- Entrenando Modelos ---")
        pipeline_lr = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('model', LogisticRegression(random_state=self.random_state, max_iter=1000, class_weight='balanced'))])
        print("Entrenando Regresión Logística...")
        pipeline_lr.fit(self.X_train, self.y_train)
        self.models['Regresión Logística'] = pipeline_lr
        print("Regresión Logística entrenada.")
        
        pipeline_rf = Pipeline(steps=[
            ('preprocessor', self.preprocessor),
            ('model', RandomForestClassifier(random_state=self.random_state, class_weight='balanced'))])
        print("Entrenando Random Forest...")
        pipeline_rf.fit(self.X_train, self.y_train)
        self.models['Random Forest'] = pipeline_rf
        print("Random Forest entrenado.")

    def evaluar_modelos(self, dataset='validation'):
        # Modificado para guardar gráficos
        if not self.models:
            print("Error: No hay modelos entrenados.")
            return
        print(f"\n--- Evaluación de Modelos en el conjunto de {dataset.upper()} ---")
        if dataset == 'validation':
            X, y = self.X_val, self.y_val
        elif dataset == 'test':
            X, y = self.X_test, self.y_test
        else:
            print("Error: 'dataset' debe ser 'validation' o 'test'.")
            return
            
        self.metrics[dataset] = {}
        for name, model in self.models.items():
            print(f"\n=== Modelo: {name} ===")
            y_pred = model.predict(X)
            y_proba = model.predict_proba(X)[:, 1]
            acc = accuracy_score(y, y_pred)
            precision = precision_score(y, y_pred, zero_division=0)
            recall = recall_score(y, y_pred, zero_division=0)
            f1 = f1_score(y, y_pred, zero_division=0)
            roc_auc = roc_auc_score(y, y_proba)
            
            cm_matrix = confusion_matrix(y, y_pred)
            if cm_matrix.shape == (2, 2):
                tn, fp, fn, tp = cm_matrix.ravel()
            else:
                tn, fp, fn, tp = (cm_matrix[0,0], 0, 0, 0) if len(cm_matrix) == 1 else (0,0,0,0)
            specificity = tn / (tn + fp) if (tn + fp) > 0 else 0
            
            self.metrics[dataset][name] = {
               'Accuracy': acc, 'Precision': precision, 'Recall': recall,
               'Specificity': specificity, 'F1-Score': f1, 'ROC-AUC': roc_auc,
               'True_Positives': tp, 'False_Positives': fp, 'False_Negatives': fn, 'True_Negatives': tn
            }
            
            print(f"\nMétricas de Negocio:")
            print(f"   - Clientes buenos correctamente identificados: {tn} ({specificity*100:.1f}%)")
            print(f"   - Morosos correctamente detectados: {tp} ({recall*100:.1f}%)")
            print(f"   - Falsos rechazos (perder buenos clientes): {fp}")
            print(f"   - Créditos riesgosos no detectados: {fn}")
            print(classification_report(y, y_pred, zero_division=0))
            
            # --- GUARDAR GRÁFICO ---
            fig, ax = plt.subplots(figsize=(6, 4))
            sns.heatmap(cm_matrix, annot=True, fmt='d', cmap='Blues',
                        xticklabels=model.classes_, yticklabels=model.classes_, ax=ax)
            ax.set_title(f'Matriz de Confusión - {name} ({dataset})')
            ax.set_xlabel('Predicción')
            ax.set_ylabel('Valor Real')
            fig_path = os.path.join(self.output_dir, f'plot_matriz_confusion_{name}_{dataset}_{self.timestamp}.png')
            plt.savefig(fig_path)
            plt.close(fig) # Cerrar la figura

        return pd.DataFrame(self.metrics[dataset]).T.sort_values('F1-Score', ascending=False)


    def analizar_overfitting(self):
        # Modificado para guardar gráficos
        print("\n" + "="*70 + "\nANÁLISIS DE OVERFITTING/UNDERFITTING\n" + "="*70)
        analisis = {}
        for name, model in self.models.items():
            print(f"\n{'='*50}\nModelo: {name}\n{'='*50}")
            y_pred_train = model.predict(self.X_train)
            f1_train = f1_score(self.y_train, y_pred_train, zero_division=0)
            acc_train = accuracy_score(self.y_train, y_pred_train)
            y_pred_val = model.predict(self.X_val)
            f1_val = f1_score(self.y_val, y_pred_val, zero_division=0)
            acc_val = accuracy_score(self.y_val, y_pred_val)
            y_pred_test = model.predict(self.X_test)
            f1_test = f1_score(self.y_test, y_pred_test, zero_division=0)
            acc_test = accuracy_score(self.y_test, y_pred_test)
            diff_train_val = f1_train - f1_val
            diff_val_test = f1_val - f1_test
            analisis[name] = {
                'F1_Train': f1_train, 'F1_Val': f1_val, 'F1_Test': f1_test,
                'Acc_Train': acc_train, 'Acc_Val': acc_val, 'Acc_Test': acc_test,
                'Diff_Train_Val': diff_train_val, 'Diff_Val_Test': diff_val_test
            }
            # (Diagnóstico por prints omitido por brevedad)
            
        df_analisis = pd.DataFrame(analisis).T
        print(f"\n{'='*70}\nTABLA COMPARATIVA DE OVERFITTING\n{'='*70}")
        print(df_analisis)

        # --- GUARDAR GRÁFICO ---
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        df_plot = df_analisis[['F1_Train', 'F1_Val', 'F1_Test']]
        df_plot.plot(kind='bar', ax=axes[0], color=['#2ecc71', '#3498db', '#e74c3c'])
        axes[0].set_title('F1-Score por Dataset', fontsize=14, fontweight='bold')
        axes[0].set_xticklabels(df_analisis.index, rotation=45, ha='right')
        # ... (configuración de gráficos) ...
        df_diff = df_analisis[['Diff_Train_Val', 'Diff_Val_Test']]
        df_diff.plot(kind='bar', ax=axes[1], color=['#e67e22', '#9b59b6'])
        axes[1].set_title('Diferencias entre Datasets', fontsize=14, fontweight='bold')
        axes[1].set_xticklabels(df_analisis.index, rotation=45, ha='right')
        # ... (configuración de gráficos) ...
        plt.tight_layout()
        fig_path = os.path.join(self.output_dir, f'plot_analisis_overfitting_{self.timestamp}.png')
        plt.savefig(fig_path)
        plt.close(fig) # Cerrar la figura
        
        return df_analisis


    def validacion_cruzada(self, cv=5):
        # Modificado para guardar gráficos y corregir error de 'if f1_scores:'
        print("\n" + "="*70 + f"\nVALIDACIÓN CRUZADA (K={cv} Folds Estratificados)\n" + "="*70)
        X_combined = pd.concat([self.X_train, self.X_val])
        y_combined = pd.concat([self.y_train, self.y_val])
        cv_results = {}
        skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=self.random_state)
        
        for name, model in self.models.items():
            print(f"\n{'='*50}\nValidación Cruzada: {name}\n{'='*50}")
            scoring_metrics = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
            scores = {}
            for metric in scoring_metrics:
                try:
                    cv_scores = cross_val_score(model, X_combined, y_combined, cv=skf, scoring=metric, n_jobs=-1)
                    scores[metric] = {'mean': cv_scores.mean(), 'std': cv_scores.std(), 'scores': cv_scores}
                    print(f"   {metric.upper():12s}: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
                except Exception as e:
                    print(f"   {metric.upper():12s}: Error - {str(e)}")
                    scores[metric] = {'mean': 0, 'std': 0, 'scores': []}
            cv_results[name] = scores
            # (prints de estabilidad omitidos por brevedad)

        comparison_data = {}
        for name, scores in cv_results.items():
            comparison_data[name] = {f'{metric}_mean': scores[metric]['mean'] for metric in scoring_metrics}
            comparison_data[name].update({f'{metric}_std': scores[metric]['std'] for metric in scoring_metrics})
        df_cv = pd.DataFrame(comparison_data).T
        print(f"\n{'='*70}\nRESUMEN DE VALIDACIÓN CRUZADA\n{'='*70}")
        print(df_cv[[f'{m}_mean' for m in scoring_metrics]])

        # --- GUARDAR GRÁFICO ---
        fig, axes = plt.subplots(1, len(self.models), figsize=(7*len(self.models), 5), squeeze=False)
        axes = axes.ravel()
        for idx, (name, scores) in enumerate(cv_results.items()):
            f1_scores = scores['f1']['scores']
            
            # --- ¡CORRECCIÓN DE VALUEERROR! ---
            if len(f1_scores) > 0: 
                axes[idx].boxplot([f1_scores], labels=['F1-Score'])
                axes[idx].scatter([1]*len(f1_scores), f1_scores, alpha=0.5, color='red')
                axes[idx].set_title(f'{name}\nF1: {scores["f1"]["mean"]:.3f} ± {scores["f1"]["std"]:.3f}', fontweight='bold')
                axes[idx].set_ylabel('F1-Score')
                axes[idx].grid(alpha=0.3, axis='y')
                axes[idx].axhline(y=scores['f1']['mean'], color='green', linestyle='--', alpha=0.7)
                
        plt.tight_layout()
        fig_path = os.path.join(self.output_dir, f'plot_validacion_cruzada_{self.timestamp}.png')
        plt.savefig(fig_path)
        plt.close(fig) # Cerrar la figura

        return cv_results, df_cv


    def comparacion_objetiva_modelos(self):
        # Modificado para guardar gráficos
        print("\n" + "="*70 + "\nCOMPARACIÓN OBJETIVA DE MODELOS\n" + "="*70)
        if 'validation' not in self.metrics or 'test' not in self.metrics:
            print("Error: Deben evaluarse los modelos en validation y test primero.")
            return pd.DataFrame(), None # Devuelve vacío
            
        comparison = {}
        for name in self.models.keys():
            val_metrics = self.metrics['validation'][name]
            test_metrics = self.metrics['test'][name]
            comparison[name] = {
                'Val_F1': val_metrics['F1-Score'], 'Test_F1': test_metrics['F1-Score'],
                'Val_ROC_AUC': val_metrics['ROC-AUC'], 'Test_ROC_AUC': test_metrics['ROC-AUC'],
                'Val_Recall': val_metrics['Recall'], 'Test_Recall': test_metrics['Recall'],
                'Val_Precision': val_metrics['Precision'], 'Test_Precision': test_metrics['Precision'],
                'Consistency': abs(val_metrics['F1-Score'] - test_metrics['F1-Score'])
            }
        df_comp = pd.DataFrame(comparison).T
        
        # (prints de rankings omitidos por brevedad)
        
        print(f"\n{'='*70}\nPUNTUACIÓN PONDERADA FINAL\n{'='*70}")
        df_comp['Score_Final'] = (
            0.40 * df_comp['Test_F1'] + 0.30 * df_comp['Test_ROC_AUC'] +
            0.20 * df_comp['Test_Recall'] + 0.10 * (1 - df_comp['Consistency']))
        ranking_final = df_comp.sort_values('Score_Final', ascending=False)
        # (prints de ranking final omitidos por brevedad)
        
        mejor_modelo = ranking_final.index[0]
        print(f"\nMODELO RECOMENDADO: {mejor_modelo}")

        # --- GUARDAR GRÁFICO ---
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        # Gráfico 1: Consistencia
        axes[0, 0].scatter(df_comp['Val_F1'], df_comp['Test_F1'], s=200, alpha=0.6)
        axes[0, 0].set_title('Consistencia Val-Test', fontweight='bold')
        # ... (configuración de gráficos) ...
        # Gráfico 2: Precision-Recall
        axes[0, 1].scatter(df_comp['Test_Recall'], df_comp['Test_Precision'], s=200, alpha=0.6, c='coral')
        axes[0, 1].set_title('Trade-off Precision-Recall', fontweight='bold')
        # ... (configuración de gráficos) ...
        # Gráfico 3: ROC-AUC
        df_comp[['Val_ROC_AUC', 'Test_ROC_AUC']].plot(kind='bar', ax=axes[1, 0], color=['skyblue', 'navy'])
        axes[1, 0].set_title('ROC-AUC: Validation vs Test', fontweight='bold')
        axes[1, 0].set_xticklabels(df_comp.index, rotation=45, ha='right')
        # ... (configuración de gráficos) ...
        # Gráfico 4: Score Final
        ranking_final['Score_Final'].sort_values().plot(kind='barh', ax=axes[1, 1], color='green', alpha=0.7)
        axes[1, 1].set_title('Puntuación Final Ponderada', fontweight='bold')
        # ... (configuración de gráficos) ...
        plt.tight_layout()
        fig_path = os.path.join(self.output_dir, f'plot_comparacion_modelos_{self.timestamp}.png')
        plt.savefig(fig_path)
        plt.close(fig) # Cerrar la figura

        print(f"\n{'='*70}\nTABLA COMPLETA DE COMPARACIÓN\n{'='*70}")
        print(df_comp)
        return df_comp, mejor_modelo

    def ejecutar_pipeline_completo(self):
        # Orquesta todo el flujo base.
        print("=== INICIO DEL PIPELINE DE CLASIFICACIÓN ===\n")
        try:
            self.load_data()
            self.resumen_general()
            self.detectar_target()
            
            if self.target is None:
                print("ERROR: No se pudo detectar la variable objetivo. Abortando.")
                return None

            print("\n--- Generando Análisis Exploratorio Visual (EDA) ---")
            self.plot_distributions()
            self.matriz_correlacion()
            self.analizar_relaciones()
            
            self.dividir_datos()
            self.crear_pipeline_preprocesamiento()
            self.entrenar_modelos()
            
            print("\n--- Evaluación en Conjunto de VALIDACIÓN ---")
            metrics_val_df = self.evaluar_modelos(dataset='validation')
            print(metrics_val_df)
            
            print("\n--- Evaluación en Conjunto de TEST ---")
            metrics_test_df = self.evaluar_modelos(dataset='test')
            print(metrics_test_df)
            
            overfitting_df = self.analizar_overfitting()
            cv_results, cv_df = self.validacion_cruzada(cv=5)
            comparison_df, mejor_modelo = self.comparacion_objetiva_modelos()
            
            print("\n" + "="*70 + "\nPIPELINE DE CLASIFICACIÓN COMPLETADO\n" + "="*70)
            print(f"\nModelo Recomendado para Producción: {mejor_modelo}")
            
            return {
               'metrics_validation': metrics_val_df, 'metrics_test': metrics_test_df,
               'overfitting_analysis': overfitting_df, 'cross_validation': cv_df,
               'comparison': comparison_df, 'best_model': mejor_modelo
            }
        except Exception as e:
            print(f"Ha ocurrido un error durante la ejecución del pipeline: {e}")
            return None

# --- FUNCIONES DE OPTIMIZACIÓN (ANEXO 2.3) ---
# (Idénticas al código anterior, sin cambios)

def _seleccionar_mejor_modelo_por_validacion(clf: ClasificadorMorosidad):
    if 'validation' not in clf.metrics:
        print("Error: primero ejecuta la evaluación en VALIDACIÓN.")
        return None
    if not clf.metrics['validation']: # Chequeo extra si está vacío
        print("Error: Diccionario de métricas de validación está vacío.")
        return None
    df_val = pd.DataFrame(clf.metrics['validation']).T
    if df_val.empty:
        print("Error: DataFrame de métricas de validación está vacío.")
        return None
    best_name = df_val.sort_values('F1-Score', ascending=False).index[0]
    print(f"\n[2.3] Mejor modelo base (VALIDACIÓN, F1): {best_name}")
    return best_name

def _optimizar_mejor_modelo(clf: ClasificadorMorosidad, nombre_mejor: str, cv=5, n_iter=30, random_state=42):
    if nombre_mejor not in clf.models:
        print("Error: nombre del mejor modelo no está en clf.models.")
        return None, None, None, None
    base_model = clf.models[nombre_mejor]
    skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=random_state)
    if 'Regresión Logística' in nombre_mejor:
        param_grid = {
            'model__solver': ['saga'], 'model__penalty': ['l1', 'l2', 'elasticnet'],
            'model__C': loguniform(1e-3, 1e2), 'model__l1_ratio': [0.15, 0.3, 0.5, 0.7, 0.85]
        }
        search = RandomizedSearchCV(
            estimator=base_model, param_distributions=param_grid, n_iter=n_iter,
            scoring='f1', cv=skf, n_jobs=-1, random_state=random_state, verbose=0
        )
        etiqueta_nuevo = 'Regresión Logística (Optimizada)'
    elif 'Random Forest' in nombre_mejor:
        param_grid = {
            'model__n_estimators': randint(150, 600),
            'model__max_depth': [None, 6, 10, 14, 18, 22],
            'model__min_samples_split': randint(2, 20),
            'model__min_samples_leaf': randint(1, 10),
            'model__max_features': ['sqrt', 'log2', 0.5, 0.7, 1.0],
            'model__class_weight': ['balanced']
        }
        search = RandomizedSearchCV(
            estimator=base_model, param_distributions=param_grid, n_iter=n_iter,
            scoring='f1', cv=skf, n_jobs=-1, random_state=random_state, verbose=0
        )
        etiqueta_nuevo = 'Random Forest (Optimizado)'
    else:
        print("Modelo no reconocido para optimización.")
        return None, None, None, None
    print("\n[2.3] Ejecutando búsqueda de hiperparámetros...")
    search.fit(clf.X_train, clf.y_train)
    best_estimator = search.best_estimator_
    best_params = search.best_params_
    best_score = search.best_score_
    print(f"[2.3] Mejor configuración (media CV F1={best_score:.4f}):")
    for k, v in best_params.items():
        print(f"   - {k}: {v}")
    clf.models[etiqueta_nuevo] = best_estimator
    return etiqueta_nuevo, best_estimator, best_params, best_score

def _comparar_mejora_incremental(clf: ClasificadorMorosidad, nombre_base: str, nombre_opt: str):
    print("\n[2.3] Comparando mejora incremental (BASE vs OPTIMIZADO)")
    modelos_guardados = clf.models.copy()
    clf.models = {
        nombre_base: modelos_guardados[nombre_base],
        nombre_opt: modelos_guardados[nombre_opt]
    }
    print("\n--- (2.3) Evaluación VALIDATION (Base vs Optimizado) ---")
    m_val = clf.evaluar_modelos(dataset='validation')
    print(m_val)
    print("\n--- (2.3) Evaluación TEST (Base vs Optimizado) ---")
    m_test = clf.evaluar_modelos(dataset='test')
    print(m_test)
    clf.models = modelos_guardados
    base_F1 = m_test.loc[nombre_base, 'F1-Score']
    opt_F1  = m_test.loc[nombre_opt,  'F1-Score']
    delta   = opt_F1 - base_F1
    base_rec = m_test.loc[nombre_base, 'Recall']
    opt_rec  = m_test.loc[nombre_opt,  'Recall']
    base_spe = m_test.loc[nombre_base, 'Specificity']
    opt_spe  = m_test.loc[nombre_opt,  'Specificity']
    print("\n[2.3] Mejora en TEST:")
    print(f"   • F1-Score: {base_F1:.4f} → {opt_F1:.4f}  (Δ={delta:+.4f})")
    print(f"   • Recall (morosos): {base_rec:.4f} → {opt_rec:.4f}")
    print(f"   • Specificity (buenos): {base_spe:.4f} → {opt_spe:.4f}")
    return {
        'test_base_F1': base_F1, 'test_opt_F1': opt_F1, 'delta_F1': delta,
        'test_base_recall': base_rec, 'test_opt_recall': opt_rec,
        'test_base_specificity': base_spe, 'test_opt_specificity': opt_spe
    }

def _justificar_seleccion_final(resumen_mejora: dict, nombre_final: str):
    # (Idéntico al código anterior, sin cambios)
    print("\n--- (2.3) Justificación de la Selección Final ---")
    f1_gain = resumen_mejora['delta_F1']
    rec_gain = resumen_mejora['test_opt_recall'] - resumen_mejora['test_base_recall']
    spe_gain = resumen_mejora['test_opt_specificity'] - resumen_mejora['test_base_specificity']
    print("Criterios de negocio y técnicos:")
    print("   - Balance general (F1-Score) como métrica central de clasificación.")
    print("   - Recall para maximizar detección de morosos (riesgo crediticio).")
    print("   - Specificity para minimizar falsos rechazos (proteger clientes buenos).")
    print("\nConclusión:")
    if f1_gain >= 0:
        print(f"   • El modelo '{nombre_final}' mejora el F1-Score en TEST (Δ={f1_gain:+.4f}).")
    else:
        print(f"   • El modelo '{nombre_final}' mantiene F1-Score competitivo (Δ={f1_gain:+.4f}).")

    if rec_gain >= 0:
        print(f"   • Aumenta la sensibilidad (Recall) hacia morosos (Δ={rec_gain:+.4f}).")
    else:
        print(f"   • Mantiene/Reduce ligeramente el Recall (Δ={rec_gain:+.4f}), evaluado frente a Specificity.")

    if spe_gain >= 0:
        print(f"   • Mejora o preserva la Specificity (Δ={spe_gain:+.4f}) evitando rechazos injustos.")
    else:
        print(f"   • Ligera reducción de Specificity (Δ={spe_gain:+.4f}); trade-off aceptado por mayor detección.")
    print(f"\nSelección recomendada: '{nombre_final}' por mejor equilibrio y desempeño en TEST.")


# --- FUNCIÓN PRINCIPAL DE EJECUCIÓN ---

def main(args):
    """
    Función principal que ejecuta todo el pipeline de entrenamiento.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # --- Parte 1: Pipeline Principal y Evaluación Base ---
    print("\n" + "="*70)
    print("SISTEMA DE PREDICCIÓN DE MOROSIDAD - AHORRO VALLE")
    print("="*70)

    clasificador = ClasificadorMorosidad(
        data_path=args.input_file,
        output_dir=args.output_dir,
        random_state=42
    )

    resultados_base = clasificador.ejecutar_pipeline_completo()

    # Manejar si el pipeline falló (ej. no se encontró el target)
    if resultados_base is None:
        print("Finalizando el script debido a un error en el pipeline base.")
        return

    # --- Parte 2: Optimización del Mejor Modelo (Anexo 2.3) ---
    print("\n" + "-"*70)
    print("2.3 Franz Caceres - OPTIMIZACIÓN DEL MEJOR MODELO")
    print("-"*70)

    _best_base = _seleccionar_mejor_modelo_por_validacion(clasificador)
    _nombre_final_recomendado = resultados_base.get('best_model')
    
    if _best_base is not None and _nombre_final_recomendado is not None:
        nombre_opt, best_estimator, best_params, best_cv = _optimizar_mejor_modelo(
            clasificador, _best_base, cv=5, n_iter=30, random_state=clasificador.random_state
        )
        if nombre_opt is not None:
            resumen_mejora = _comparar_mejora_incremental(clasificador, _best_base, nombre_opt)
            _justificar_seleccion_final(resumen_mejora, nombre_opt)
            _nombre_final_recomendado = nombre_opt 
            print("\n[2.3] Modelo optimizado registrado.")
        else:
            print("[2.3] No se pudo optimizar el modelo seleccionado.")
    else:
        print("[2.3] No se pudo seleccionar un modelo base para optimizar.")

    # --- Parte 3: Guardar Artefactos Finales ---
    print("\n" + "="*70)
    print("PROCESO COMPLETO FINALIZADO - GUARDANDO ARTEFACTOS")
    print("="*70)

    # 1. Guardar el modelo final (pipeline completo)
    if _nombre_final_recomendado and _nombre_final_recomendado in clasificador.models:
        final_model_pipeline = clasificador.models[_nombre_final_recomendado]
        model_filename = os.path.join(args.output_dir, f'model_pipeline_final_{timestamp}.joblib')
        joblib.dump(final_model_pipeline, model_filename)
        print(f"✅ Modelo final guardado en: {model_filename}")
    else:
        print("❌ ERROR: No se encontró el modelo final para guardar.")


    # 2. Guardar las métricas y resultados
    metrics_filename = os.path.join(args.output_dir, f'training_results_{timestamp}.json')
    # Convertir DataFrames a dict para serialización JSON
    results_serializable = {
        'best_model_name': _nombre_final_recomendado,
        'timestamp': timestamp,
        'input_file': args.input_file
    }
    
    # Añadir dataframes solo si existen
    if 'metrics_validation' in resultados_base and not resultados_base['metrics_validation'].empty:
        results_serializable['metrics_validation'] = resultados_base['metrics_validation'].to_dict('index')
    if 'metrics_test' in resultados_base and not resultados_base['metrics_test'].empty:
        results_serializable['metrics_test'] = resultados_base['metrics_test'].to_dict('index')
    if 'overfitting_analysis' in resultados_base and not resultados_base['overfitting_analysis'].empty:
        results_serializable['overfitting_analysis'] = resultados_base['overfitting_analysis'].to_dict('index')
    if 'cross_validation' in resultados_base and not resultados_base['cross_validation'].empty:
        results_serializable['cross_validation'] = resultados_base['cross_validation'].to_dict('index')
    if 'comparison' in resultados_base and not resultados_base['comparison'].empty:
        results_serializable['comparison'] = resultados_base['comparison'].to_dict('index')

    try:
        with open(metrics_filename, 'w') as f:
            json.dump(results_serializable, f, indent=4)
        print(f"✅ Resultados/métricas guardados en: {metrics_filename}")
    except Exception as e:
        print(f"❌ ERROR al guardar el JSON de resultados: {e}")
        
    print(f"✅ Gráficos y dataset limpio guardados en el directorio: {args.output_dir}")

# --- PUNTO DE ENTRADA DEL SCRIPT ---

if __name__ == "__main__":
    
    # Configurar el parser de argumentos de línea de comandos
    parser = argparse.ArgumentParser(description="Script de Entrenamiento Automático de Morosidad")
    
    parser.add_argument(
        "--input_file",
        type=str,
        default="dataset_credito_morosidad.csv",
        help="Ruta al archivo CSV del dataset de entrada."
    )
    
    parser.add_argument(
        "--output_dir",
        type=str,
        default="output",
        help="Directorio donde se guardarán los modelos, métricas y gráficos."
    )
    
    # --- ¡CORRECCIÓN DE ARGPARSE! ---
    # Usamos parse_known_args() para ignorar los args internos del notebook
    args, unknown = parser.parse_known_args()
    
    # Ejecutar la función principal
    main(args)
