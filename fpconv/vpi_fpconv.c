/*
Prototype for creating a frequency distribution of the signals during a simulation.
At the start of the simulation, the hierarchy of the design is explored and full signal names are read.
During the simulation, values of the signals are read and the distribution table is updated.
*/

#include <assert.h>
#include <stdio.h>
#include <vpi_user.h>

void register_cb(
  PLI_INT32(*f)(p_cb_data),
  PLI_INT32 reason
){
  s_cb_data cbData;
  cbData.time = NULL;
  cbData.reason = reason;
  cbData.cb_rtn = f;
  cbData.user_data = 0;
  cbData.value = 0;
  assert(vpi_register_cb(&cbData) != NULL);
}

void printContent(vpiHandle parent) {
  vpi_printf("- %s", vpi_get_str (vpiName, parent));
  vpi_printf(" [%s]\n", vpi_get_str (vpiFullName, parent));

  vpiHandle Iterator;
  vpiHandle hnd;

  // TODO Is it possible to get the type of the signal/port?

  Iterator = vpi_iterate(vpiPort, parent);
  assert(Iterator != NULL);
  while (hnd = vpi_scan (Iterator))
    vpi_printf("  + %s [dir %d]\n", (char*) vpi_get_str(vpiName, hnd), vpi_get(vpiDirection, hnd));

  Iterator = vpi_iterate(vpiNet, parent);
  assert(Iterator != NULL);
  while (hnd = vpi_scan (Iterator))
    vpi_printf("  + %s\n", (char*) vpi_get_str(vpiName, hnd));

  Iterator = vpi_iterate(vpiModule, parent);
  assert(Iterator != NULL);
  while ((hnd = vpi_scan (Iterator)))
    printContent(hnd);
}

PLI_INT32 startCallback(p_cb_data data){
  vpiHandle topIterator = vpi_iterate (vpiModule, NULL);
  assert(topIterator != NULL);

  vpiHandle topHandle;
  while ((topHandle = vpi_scan(topIterator)))
    printContent(topHandle);

  return 0;
}

// TODO Instead of getting the value(s) at the end, do it:
// - Periodically
// - or, when a signal changes (register event callback?)
PLI_INT32 endCallback(p_cb_data data){
  vpiHandle hnd = vpi_handle_by_name("tb.inst.cnt", NULL);
  assert(hnd != NULL);

  s_vpi_value val;
  // TODO Is it possible to know the type from the handle?
  val.format = vpiBinStrVal;
  vpi_get_value(hnd, &val);
  printf("%s tb.inst.cnt\n", val.value.str);
  return 0;
}

void entry_point_cb() {
  register_cb(startCallback, cbStartOfSimulation);
  register_cb(endCallback, cbEndOfSimulation);
}

void (*vlog_startup_routines[]) () = {entry_point_cb, 0};
