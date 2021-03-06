import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

inp = ['data/train_data.csv', 'data/val_data.csv', 'data/test_data.csv']


def check_intercepted_data(list_of_files):
    """ Checks if the training, validating and testing data files overlap
    each other, and prints the results :param list_of_files: list containing
    the names of the data files
    """

    interception_results = 'Interception results:'
    num_of_overlaps = 0

    # for each file, reads the 'loc string' column values and inserts them
    # into a numpy Array
    train_array = pd.read_csv(list_of_files[0])['loc_string'].to_numpy()
    val_array = pd.read_csv(list_of_files[1])['loc_string'].to_numpy()
    test_array = pd.read_csv(list_of_files[2])['loc_string'].to_numpy()

    # check if the arrays overlap each other
    if np.intersect1d(train_array, val_array).size > 0:
        interception_results += '\n train overlaps with val'
        num_of_overlaps += 1
    if np.intersect1d(train_array, test_array).size > 0:
        interception_results += '\n train overlaps with test'
        num_of_overlaps += 1
    if np.intersect1d(test_array, val_array).size > 0:
        interception_results += '\n test overlaps with val'
        num_of_overlaps += 1
    if num_of_overlaps == 0:
        interception_results += '\n There are no overlaps'

    print(interception_results)


def is_variation_length_ok(list_of_files):
    """
    Checks if all the genetic variation lengths of each data file equals 1
    :param list_of_files: list containing the names of the data files
    :return: bool: True if all lengths are 1
    """

    # Read train, valid and test data
    train_data = pd.read_csv(list_of_files[0])
    val_data = pd.read_csv(list_of_files[1])
    test_data = pd.read_csv(list_of_files[2])

    # Concat all data files into a dataframe 'all_data'
    all_data = pd.concat([train_data, val_data, test_data])

    # Create a series of length of each genetic variation
    length_series = all_data['end'] - all_data['start']

    # Return True if all lengths are 1, Return False if any of the lengths is
    # different from 1
    return all(length_series == 1)


def distribution_of_genotypes_plots(list_of_files):
    """
    For each data file(train, val and test) prints normalized bar plots of
    genotype distribution, for father, mother and child.
    :param list_of_files: list containing the names of the data files.
    """

    # Create dataframes out of train, val and test data csv files
    train = pd.read_csv(list_of_files[0])
    val = pd.read_csv(list_of_files[1])
    test = pd.read_csv(list_of_files[2])

    def plot_genotype_distribution(title, df):
        """
        Prints normalized bar plots of genotype distribution.
        :param title: will be set as the title of the plot (string)
        :param df: the dataframe (train, val, test)
        """
        # From data file: get father's mother's and child's genotypes
        # distribution
        distribution_father = df['H12148W'].value_counts().sort_index()
        distribution_mother = df['M12148W'].value_counts().sort_index()
        distribution_child = df['label'].value_counts().sort_index()

        # Concat the dataframes genotype distribution of: father, mother and
        # child into a single dataframe
        dist_concat = pd.concat([distribution_father,
                                 distribution_mother,
                                 distribution_child], axis=1)

        # Convert counts into percentage out of all samples, and bar plot the
        # dataframe
        ax = (dist_concat / dist_concat.sum()[0]).plot(kind='bar',
                                                       title='Distribution of '
                                                             'Genotypes - ' +
                                                             title)

        # Set y ticks as percentage instead of a simple number
        vals = ax.get_yticks()
        ax.set_yticklabels([f'{x:,.0%}' for x in vals])

    plot_genotype_distribution('Train data', train)
    plot_genotype_distribution('Val data', val)
    plot_genotype_distribution('Test data', test)
    plt.show()


def parents_combinations_genotypes_all_plots(list_of_files):
    """
    Apply the function 'parents_combinations_genotypes_plot' for
    each data file (Train, Val, Test)
    :param list_of_files:
    :return:
    """

    # Create dataframes out of train, val and test data csv files
    train = pd.read_csv(list_of_files[0])
    val = pd.read_csv(list_of_files[1])
    test = pd.read_csv(list_of_files[2])

    def parents_combinations_genotypes_plot(title, df):
        """
        Prints a normalized heatmap of parents genotypes combinations
        :param title: will be set as the title of the plot (string)
        :param df: the dataframe (train, val, test)
        """

        # Create df that contains the number of each of the parents'
        # genotypes combination
        genotype_combination_count = df.groupby(['H12148W', 'M12148W']).size()

        # Create df with normalized values of genotype_combination_count
        genotype_combination_normal = genotype_combination_count.unstack() \
                                      / genotype_combination_count.sum()

        # Print a heatmap of the normalized df with percentage format
        sns.heatmap(genotype_combination_normal,
                    annot=True, fmt=".0%", cmap='Reds'
                    , cbar_kws={'ticks': [0, 1]}, vmax=1, vmin=0)

        plt.title(title)
        plt.show()

    parents_combinations_genotypes_plot(
        'Genotypes combinations distribution: Train', train)
    parents_combinations_genotypes_plot(
        'Genotypes combinations distribution: Val', val)
    parents_combinations_genotypes_plot(
        'Genotypes combinations distribution: Test', test)


def parents_and_child_genotype_corr_pie_plots_for_all_data(list_of_files):
    """
    Apply the function 'parents_combinations_genotypes_plot' for
    each data file (Train, Val, Test)
    :param list_of_files: list containing the names of the data files
    """

    # Create dataframes out of train, val and test data csv files
    train = pd.read_csv(list_of_files[0])
    val = pd.read_csv(list_of_files[1])
    test = pd.read_csv(list_of_files[2])

    def parents_and_child_genotype_corr_pie_plots(title, df):
        """
        For each of the the parents genotype combination, prints pie plots of
        child's genotype distribution (0/1/2).
        :param title: will be set as the title of the plot (string)
        :param df: the dataframe (train, val, test)
        """

        # Create a dataframe that it's values are the sum of the child's
        # genotype (0/1/2) for each of the parents' genotype combination
        agg_by_counts = \
            df.groupby(['H12148W', 'M12148W']).agg(
                p0=pd.NamedAgg(column='label',
                               aggfunc=lambda s: (s == 0).sum()),
                p1=pd.NamedAgg(column='label',
                               aggfunc=lambda s: (s == 1).sum()),
                p2=pd.NamedAgg(column='label', aggfunc=lambda s: (s == 2).sum())
            )

        # In order to iterate over the df values, and to create a pie plot
        # for each parents' genotype combination using 2 for loops,
        # the df must contain a row with the indexes (0,0)
        agg_by_counts.loc[(0, 0), :] = 0

        # Create a figure with 9 axes (3X3)
        fig, axs = plt.subplots(3, 3, figsize=(9, 9))

        # For every axs on the figure, create a pie chart of the child's
        # genotype distribution based on the parents genotype combination
        for i in range(3):
            for j in range(3):

                # Where parents' genotype combination is 0:0, manually fill the
                # axs with a pie chart that shows that the child's genotype
                # distribution is 100% 0, because its a known fact.
                if i == 0 and j == 0:
                    axs[i, j].pie(np.array([1]), autopct=lambda x:
                    f'{x / 100:.0%}' if x > 5 else '')
                    axs[i, j].set_title(f'Father: {i}\nMother: {j}')
                else:
                    axs[i, j].pie(agg_by_counts.loc[i, j].to_numpy(),
                                  autopct=lambda x: f'{x / 100:.0%}'
                                  if x > 5 else '')
                    axs[i, j].set_title(f'Father: {i}\nMother: {j}')

        plt.legend(title="Labels:", bbox_to_anchor=(-0.5, 0), labels=[0, 1, 2])
        fig.suptitle("Child's genotypes distribution for every parents"
                     " genotype combination - " + title)
        plt.show()

    parents_and_child_genotype_corr_pie_plots('Train', train)
    parents_and_child_genotype_corr_pie_plots('Val', val)
    parents_and_child_genotype_corr_pie_plots('Test', test)
