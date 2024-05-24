/*  ReproMPI Benchmark
 *
 *  Copyright 2015 Alexandra Carpen-Amarie, Sascha Hunold
    Research Group for Parallel Computing
    Faculty of Informatics
    Vienna University of Technology, Austria

<license>
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
</license>
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "mpi.h"

#include "reprompi_bench/sync/process_sync/process_synchronization.h"
#include "barrier_sync_common.h"
#include "dissem_barrier_impl.h"

static void dissem_barrier_print_sync_parameters(FILE* f) {
  fprintf(f, "#@procsync=dissem_barrier\n");
}

void register_dissem_barrier_module(reprompib_proc_sync_module_t *sync_mod) {

  reprompi_register_common_barrier_functions(sync_mod);

  sync_mod->name = "Dissem_Barrier";
  sync_mod->procsync = REPROMPI_PROCSYNC_DISSEMBARRIER;
  sync_mod->start_sync = dissemination_barrier;
  sync_mod->print_sync_info = dissem_barrier_print_sync_parameters;
}


